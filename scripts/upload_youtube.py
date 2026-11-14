"""Upload finished, QC-passed, human-approved videos to the DEENIKIDS YouTube channel.

Safety rules built in:
  * refuses to upload if the review gate is not approved (religious + language review)
  * refuses to upload if qc_report.json is missing or failed
  * never uploads the same file twice (database/uploads.json ledger, by SHA-256)
  * every video is marked Made for Kids
  * uploads as PRIVATE by default; you publish from YouTube Studio after a final look
    (note: until your Google Cloud project passes YouTube's API audit, YouTube forces
     API uploads to private anyway)

Needs three GitHub Secrets (see README): YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

Usage:
  python scripts/upload_youtube.py bismillah-before-we-begin --lang en --what episode
  python scripts/upload_youtube.py bismillah-before-we-begin --lang hi --what all
  python scripts/upload_youtube.py bismillah-before-we-begin --what all --dry-run
"""
import argparse
import datetime as dt
import os
import sys
import time

from common import load_json, load_settings, load_song, load_storyboard, out_dir, path, save_json
from review_gate import is_approved

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]


def youtube_client():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    missing = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if missing:
        sys.exit(f"Missing secrets: {', '.join(missing)}. Add them in GitHub > Settings > Secrets and variables > Actions.")
    creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"], token_uri="https://oauth2.googleapis.com/token",
                        client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"], scopes=SCOPES)
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def plan(song, sb, lang, what):
    """List of (kind, short_id, mp4, title, description, tags)."""
    meta = song["youtube"][lang]
    items = []
    if what in ("episode", "all"):
        mp4 = os.path.join(out_dir(song["id"], "episodes"), f"{song['id']}_{lang}.mp4")
        items.append(("episode", None, mp4, meta["title"], meta["description"], meta["tags"]))
    for sh in sb.get("shorts", []):
        if what in ("shorts", "all") or what == sh["id"]:
            mp4 = os.path.join(out_dir(song["id"], "shorts"), f"{song['id']}_{lang}_short-{sh['id']}.mp4")
            items.append(("short", sh["id"], mp4, sh["title_" + lang], meta["description"], [t for t in meta["tags"] if t] + ["shorts"]))
    return items


def upload_one(yt, mp4, title, description, tags, lang, settings, publish_at=None):
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    ycfg = settings["youtube"]
    status = {"privacyStatus": ycfg["privacy_on_upload"], "selfDeclaredMadeForKids": ycfg["made_for_kids"], "embeddable": True}
    if publish_at:
        status.update({"privacyStatus": "private", "publishAt": publish_at})
    if ycfg.get("contains_synthetic_media") is not None:
        status["containsSyntheticMedia"] = ycfg["contains_synthetic_media"]
    body = {
        "snippet": {"title": title[:100], "description": description[:5000], "tags": tags, "categoryId": ycfg["category_id"],
                    "defaultLanguage": lang, "defaultAudioLanguage": lang},
        "status": status,
    }
    media = MediaFileUpload(mp4, mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    response, retries = None, 0
    while response is None:
        try:
            st, response = req.next_chunk()
            if st:
                print(f"    {int(st.progress() * 100)}%")
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504) and retries < 5:
                retries += 1
                time.sleep(2 ** retries)
                continue
            raise
    return response["id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song_id")
    ap.add_argument("--lang", default="all", help="en, hi or all")
    ap.add_argument("--what", default="all", help="episode, shorts, all, or a single short id")
    ap.add_argument("--publish-at", default=None, help="ISO time like 2026-12-01T09:00:00Z (needs audited API project)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    settings = load_settings()
    song, sb = load_song(a.song_id), load_storyboard(a.song_id)

    print("Review gate:")
    if song.get("auto"):
        ap_p = path("config", "approved_sources.json")
        approved = set(load_json(ap_p)["approved"]) if os.path.exists(ap_p) else set()
        src = song.get("source_text", "")
        if not src.startswith(("No religious", "Arabic")) and src not in approved:
            sys.exit(f"BLOCKED: source not yet approved: {src}. Add it to config/approved_sources.json after checking.")
        print("  OK (automatic song; source approved or not religious)")
    elif not is_approved(song):
        sys.exit("BLOCKED: religious/language review not approved yet. See scripts/review_gate.py")
    qc_p = os.path.join(out_dir(a.song_id), "qc_report.json")
    if not os.path.exists(qc_p) or not load_json(qc_p)["pass"]:
        sys.exit("BLOCKED: quality check missing or failed. Run scripts/quality_check.py")
    qc = {v["file"]: v for v in load_json(qc_p)["videos"]}

    ledger_p = path("database", "uploads.json")
    ledger = load_json(ledger_p) if os.path.exists(ledger_p) else {"uploads": []}
    done = {u["sha256"] for u in ledger["uploads"]}
    langs = settings["languages"] if a.lang == "all" else [a.lang]
    yt = None if a.dry_run else youtube_client()

    for lang in langs:
        for kind, short_id, mp4, title, desc, tags in plan(song, sb, lang, a.what):
            name = os.path.basename(mp4)
            if name not in qc or not qc[name]["pass"]:
                print(f"SKIP {name}: not in QC report or failed QC")
                continue
            digest = qc[name]["sha256"]
            if digest in done:
                print(f"SKIP {name}: already uploaded")
                continue
            print(f"UPLOAD {name} -> '{title}'")
            if a.dry_run:
                continue
            vid = upload_one(yt, mp4, title, desc, tags, lang, settings, a.publish_at)
            print(f"    video id {vid}")
            if kind == "episode":
                thumb = os.path.join(out_dir(a.song_id, "thumbnails"), f"{a.song_id}_{lang}.jpg")
                try:
                    from googleapiclient.http import MediaFileUpload
                    yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb, mimetype="image/jpeg")).execute()
                    print("    thumbnail set")
                except Exception as e:  # custom thumbnails need a phone-verified channel
                    print(f"    thumbnail NOT set ({e}). Verify the channel by phone, then set it in Studio.")
            playlist = settings["youtube"]["playlists"].get(lang)
            if playlist:
                yt.playlistItems().insert(part="snippet", body={"snippet": {"playlistId": playlist, "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute()
            ledger["uploads"].append({"file": name, "sha256": digest, "video_id": vid, "lang": lang, "kind": kind,
                                      "short": short_id, "uploaded_at": dt.datetime.utcnow().isoformat() + "Z"})
            save_json(ledger_p, ledger)  # save after every upload so a crash never causes a duplicate
            done.add(digest)
    print("Done.")


if __name__ == "__main__":
    main()
