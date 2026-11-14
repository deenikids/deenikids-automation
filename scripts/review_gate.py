"""Human review gate. Religious content is NEVER published until a person approves it.

To approve, edit content/songs/<song_id>/song.json and set each item under "review" to
  "status": "approved", "reviewer": "<name>", "date": "YYYY-MM-DD"
then commit. (Use "rejected" with notes if changes are needed.)

Usage: python scripts/review_gate.py bismillah-before-we-begin
Exit code 0 = approved, 1 = not approved yet.
"""
import sys

from common import load_song


def is_approved(song, verbose=True):
    ok = True
    for item, r in song.get("review", {}).items():
        good = r.get("status") == "approved" and r.get("reviewer") and r.get("date")
        if verbose:
            print(f"  {'OK     ' if good else 'WAITING'} {item}: {r.get('status')} {('by ' + r['reviewer']) if r.get('reviewer') else ''}")
        ok = ok and bool(good)
    if not song.get("religious_sources"):
        if verbose:
            print("  WAITING religious_sources: none listed")
        ok = False
    return ok


if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else "bismillah-before-we-begin"
    approved = is_approved(load_song(sid))
    print("REVIEW GATE:", "APPROVED" if approved else "NOT APPROVED - upload blocked")
    sys.exit(0 if approved else 1)
