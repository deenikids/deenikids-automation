"""2D stand-in drawings of the four DEENIKIDS characters, used by the ANIMATIC renderer.

These are simple placeholder versions of the master designs in docs/CHARACTER_BIBLE.md,
drawn with code so the pipeline can be tested end to end before the Blender models exist
(Phase 3). Colours come from the character bible so everything stays on-model.

Every draw function takes:
  d      - PIL ImageDraw
  cx, cy - centre of the character in pixels
  u      - size unit in pixels (about the height of a child character)
  st     - state dict: t, mouth (0..1), blink (bool), arm (radians), pose ('idle'|'dance'|'wave'|'wash'|'happy')
"""
import math

OUT = (30, 42, 74)          # outline navy
WHITE = (255, 255, 255)
PUPIL = (24, 28, 48)
BLUSH = (255, 150, 170)

PAL = {
    "deeni": {"body": (38, 154, 214), "belly": (255, 241, 208), "fin": (28, 128, 190), "mark": (255, 255, 255)},
    "bubbly": {"body": (255, 210, 63), "spot": (255, 168, 40), "sucker": (255, 236, 160)},
    "ayaan": {"skin": (226, 176, 130), "kurta": (46, 158, 91), "kurta_dark": (32, 120, 68), "trouser": (245, 233, 205), "cap": (255, 255, 255), "shoe": (120, 80, 50), "hair": (60, 40, 30)},
    "amira": {"skin": (232, 186, 142), "hijab": (242, 123, 168), "hijab_dark": (214, 92, 140), "dress": (249, 176, 206), "shoe": (150, 70, 110)},
}


def ell(d, cx, cy, rx, ry, fill, w=0, outline=OUT):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=outline if w else None, width=int(w))


def poly(d, pts, fill, w=0, outline=OUT):
    d.polygon(pts, fill=fill, outline=outline if w else None, width=int(w))


def eye(d, x, y, r, blink, look=0.0, happy=False):
    if happy:
        d.arc([x - r, y - r * 0.6, x + r, y + r * 0.9], 200, 340, fill=PUPIL, width=max(2, int(r * 0.3)))
        return
    if blink:
        d.line([x - r, y, x + r, y], fill=PUPIL, width=max(2, int(r * 0.25)))
        return
    ell(d, x, y, r, r * 1.1, WHITE, r * 0.12)
    ell(d, x + look * r * 0.3, y + r * 0.1, r * 0.62, r * 0.7, PUPIL)
    ell(d, x + look * r * 0.3 + r * 0.22, y - r * 0.18, r * 0.2, r * 0.2, WHITE)


def mouth(d, x, y, w, m, lw):
    """m = 0 -> closed smile, m = 1 -> wide open singing mouth."""
    if m < 0.12:
        d.arc([x - w, y - w * 0.7, x + w, y + w * 0.7], 20, 160, fill=OUT, width=max(2, int(lw)))
    else:
        h = w * (0.35 + 0.9 * m)
        d.chord([x - w * 0.9, y - h * 0.35, x + w * 0.9, y + h], 0, 180, fill=(170, 40, 60), outline=OUT, width=max(2, int(lw * 0.8)))
        d.chord([x - w * 0.55, y + h * 0.3, x + w * 0.55, y + h * 0.95], 180, 360, fill=(255, 120, 130))


def arm(d, sx, sy, length, angle, colour, hand, lw):
    ex = sx + length * math.sin(angle)
    ey = sy + length * math.cos(angle)
    d.line([sx, sy, ex, ey], fill=colour, width=int(length * 0.32), joint="curve")
    ell(d, ex, ey, length * 0.2, length * 0.2, hand, lw)
    return ex, ey


def draw_deeni(d, cx, cy, u, st):
    p = PAL["deeni"]
    s = u * 1.05
    lw = s * 0.018
    t = st["t"]
    # travelling bubble (signature feature)
    br = s * 0.78
    d.ellipse([cx - br, cy - br, cx + br, cy + br], outline=(200, 240, 255), width=int(s * 0.02))
    d.arc([cx - br * 0.8, cy - br * 0.8, cx + br * 0.8, cy + br * 0.8], 200, 250, fill=WHITE, width=int(s * 0.03))
    wag = math.sin(t * 6) * s * 0.06
    # tail
    poly(d, [(cx - s * 0.45, cy), (cx - s * 0.74, cy - s * 0.26 + wag), (cx - s * 0.64, cy + wag * 0.5), (cx - s * 0.74, cy + s * 0.24 + wag)], p["fin"], lw)
    # dorsal fin with crescent mark
    poly(d, [(cx - s * 0.08, cy - s * 0.26), (cx + s * 0.08, cy - s * 0.56), (cx + s * 0.2, cy - s * 0.24)], p["fin"], lw)
    mx, my, mr = cx + s * 0.085, cy - s * 0.36, s * 0.06
    ell(d, mx, my, mr, mr, p["mark"])
    ell(d, mx + mr * 0.45, my - mr * 0.2, mr * 0.85, mr * 0.85, p["fin"])
    # body + belly
    ell(d, cx, cy, s * 0.52, s * 0.31, p["body"], lw)
    ell(d, cx + s * 0.06, cy + s * 0.11, s * 0.4, s * 0.16, p["belly"])
    # side fin (flaps)
    flap = math.sin(t * 5) * s * 0.05
    poly(d, [(cx - s * 0.02, cy + s * 0.12), (cx - s * 0.2, cy + s * 0.34 + flap), (cx + s * 0.12, cy + s * 0.2)], p["fin"], lw)
    # face
    eye(d, cx + s * 0.22, cy - s * 0.07, s * 0.1, st["blink"], 0.4, st.get("pose") == "happy")
    ell(d, cx + s * 0.35, cy + s * 0.04, s * 0.05, s * 0.03, BLUSH)
    mouth(d, cx + s * 0.35, cy + s * 0.1, s * 0.09, st["mouth"], lw)


def draw_bubbly(d, cx, cy, u, st):
    p = PAL["bubbly"]
    s = u * 0.95
    lw = s * 0.018
    t = st["t"]
    # tentacles (wavy, behind head)
    for k in range(6):
        base_x = cx + (k - 2.5) * s * 0.11
        phase = k * 0.9
        pts = []
        for j in range(9):
            f = j / 8
            wave = math.sin(t * 4 + phase + f * 4) * s * 0.06 * f
            spread = (k - 2.5) * s * 0.06 * f
            pts.append((base_x + spread + wave, cy + s * 0.05 + f * s * 0.42))
        if st.get("pose") in ("dance", "wave") and k in (0, 5):
            lift = (1 if k == 5 else -1)
            pts = [(base_x + lift * s * 0.3 * (j / 8) + math.sin(t * 8) * s * 0.05 * (j / 8) * lift,
                    cy + s * 0.05 - s * 0.35 * (j / 8)) for j in range(9)]
        d.line(pts, fill=OUT, width=int(s * 0.115), joint="curve")
        d.line(pts, fill=p["body"], width=int(s * 0.08), joint="curve")
        tx, ty = pts[-1]
        ell(d, tx, ty, s * 0.045, s * 0.045, p["body"])
    # head
    ell(d, cx, cy - s * 0.12, s * 0.36, s * 0.33, p["body"], lw)
    for ox, oy, r in ((-0.18, -0.3, 0.05), (0.2, -0.32, 0.04), (0.02, -0.38, 0.035), (-0.24, -0.1, 0.03)):
        ell(d, cx + ox * s, cy + oy * s, r * s, r * s, p["spot"])
    eye(d, cx - s * 0.12, cy - s * 0.12, s * 0.1, st["blink"], 0.2, st.get("pose") == "happy")
    eye(d, cx + s * 0.12, cy - s * 0.12, s * 0.1, st["blink"], 0.2, st.get("pose") == "happy")
    ell(d, cx - s * 0.24, cy + s * 0.0, s * 0.05, s * 0.03, BLUSH)
    ell(d, cx + s * 0.24, cy + s * 0.0, s * 0.05, s * 0.03, BLUSH)
    mouth(d, cx, cy + s * 0.04, s * 0.09, st["mouth"], lw)


def _kid_arms(st, t):
    """Return (left_arm_angle, right_arm_angle) in radians. 0 = hanging down, + = towards screen-right."""
    pose = st.get("pose", "idle")
    if pose == "wave":
        return -0.25, math.pi * 0.85 + math.sin(t * 9) * 0.35
    if pose == "dance":
        sw = math.sin(t * math.pi * st.get("bps", 1.8))
        return -(math.pi * 0.7 - sw * 0.5), math.pi * 0.7 + sw * 0.5
    if pose == "wash":
        k = math.sin(t * 14) * 0.25
        return 0.9 + k, -0.9 - k
    if pose == "happy":  # "yay!" arms up and out
        k = math.sin(t * 6) * 0.15
        return -2.3 - k, 2.3 + k
    return -0.25 - math.sin(t * 2) * 0.05, 0.25 + math.sin(t * 2) * 0.05


def _kid_face(d, cx, hy, hr, st, lw):
    happy = st.get("pose") == "happy"
    eye(d, cx - hr * 0.4, hy - hr * 0.04, hr * 0.22, st["blink"], 0.0, happy)
    eye(d, cx + hr * 0.4, hy - hr * 0.04, hr * 0.22, st["blink"], 0.0, happy)
    ell(d, cx - hr * 0.62, hy + hr * 0.3, hr * 0.14, hr * 0.08, BLUSH)
    ell(d, cx + hr * 0.62, hy + hr * 0.3, hr * 0.14, hr * 0.08, BLUSH)
    mouth(d, cx, hy + hr * 0.4, hr * 0.26, st["mouth"], lw)


def draw_ayaan(d, cx, cy, u, st):
    p = PAL["ayaan"]
    lw = u * 0.016
    t = st["t"]
    hr = u * 0.22
    hy = cy - u * 0.25
    # legs
    for sx in (-1, 1):
        d.rectangle([cx + sx * u * 0.1 - u * 0.06, cy + u * 0.18, cx + sx * u * 0.1 + u * 0.06, cy + u * 0.4], fill=p["trouser"], outline=OUT, width=int(lw))
        ell(d, cx + sx * u * 0.12, cy + u * 0.42, u * 0.09, u * 0.045, p["shoe"], lw)
    # arms behind kurta edges
    la, ra = _kid_arms(st, t)
    shoulder_y = cy - u * 0.04
    front = st.get("pose") in ("wash", "happy")

    def arms():
        arm(d, cx - u * 0.17, shoulder_y, u * 0.24, la, p["kurta"], p["skin"], lw)
        arm(d, cx + u * 0.17, shoulder_y, u * 0.24, ra, p["kurta"], p["skin"], lw)

    if not front:
        arms()
    # kurta
    poly(d, [(cx - u * 0.16, cy - u * 0.07), (cx + u * 0.16, cy - u * 0.07), (cx + u * 0.24, cy + u * 0.24), (cx - u * 0.24, cy + u * 0.24)], p["kurta"], lw)
    d.line([cx, cy - u * 0.07, cx, cy + u * 0.08], fill=p["kurta_dark"], width=int(u * 0.02))
    for k in range(3):
        ell(d, cx, cy - u * 0.03 + k * u * 0.045, u * 0.012, u * 0.012, WHITE)
    if front:
        arms()
    # head, hair, cap
    ell(d, cx, hy, hr, hr, p["skin"], lw)
    d.chord([cx - hr * 0.95, hy - hr * 1.0, cx + hr * 0.95, hy + hr * 0.2], 180, 360, fill=p["hair"])
    d.chord([cx - hr * 0.98, hy - hr * 1.25, cx + hr * 0.98, hy - hr * 0.15], 180, 360, fill=p["cap"], outline=OUT, width=int(lw))
    for k in range(5):
        ell(d, cx - hr * 0.6 + k * hr * 0.3, hy - hr * 0.55, hr * 0.04, hr * 0.04, (210, 225, 215))
    _kid_face(d, cx, hy + hr * 0.12, hr, st, lw)


def draw_amira(d, cx, cy, u, st):
    p = PAL["amira"]
    lw = u * 0.016
    t = st["t"]
    hr = u * 0.2
    hy = cy - u * 0.25
    # long modest dress
    for sx in (-1, 1):
        ell(d, cx + sx * u * 0.1, cy + u * 0.43, u * 0.09, u * 0.045, p["shoe"], lw)
    la, ra = _kid_arms(st, t)
    shoulder_y = cy - u * 0.02
    front = st.get("pose") in ("wash", "happy")

    def arms():
        arm(d, cx - u * 0.2, shoulder_y, u * 0.25, la, p["dress"], p["skin"], lw)
        arm(d, cx + u * 0.2, shoulder_y, u * 0.25, ra, p["dress"], p["skin"], lw)

    if not front:
        arms()
    poly(d, [(cx - u * 0.16, cy - u * 0.06), (cx + u * 0.16, cy - u * 0.06), (cx + u * 0.27, cy + u * 0.41), (cx - u * 0.27, cy + u * 0.41)], p["dress"], lw)
    d.line([cx - u * 0.24, cy + u * 0.32, cx + u * 0.24, cy + u * 0.32], fill=WHITE, width=int(u * 0.02))
    # hijab: covers hair, ears and neck, drapes onto shoulders
    ell(d, cx, hy + hr * 0.25, hr * 1.42, hr * 1.55, p["hijab"], lw)
    poly(d, [(cx - hr * 1.2, hy + hr * 0.8), (cx + hr * 1.2, hy + hr * 0.8), (cx + hr * 1.0, cy - u * 0.02), (cx - hr * 1.0, cy - u * 0.02)], p["hijab"])
    d.arc([cx - hr * 1.15, hy - hr * 1.0, cx + hr * 1.15, hy + hr * 1.3], 200, 340, fill=p["hijab_dark"], width=int(lw * 1.5))
    if front:
        arms()
    # face oval framed by hijab
    ell(d, cx, hy + hr * 0.2, hr * 0.92, hr * 0.98, p["skin"], lw)
    _kid_face(d, cx, hy + hr * 0.25, hr, st, lw)


DRAW = {"deeni": draw_deeni, "bubbly": draw_bubbly, "ayaan": draw_ayaan, "amira": draw_amira}
