"""DEENIKIDS 3D pilot: Ali, rigged (real Blender armature), 5 action library, toddler room.
Usage: python blender/pilot.py save                      -> writes assets/characters/ali_pilot.blend
       python blender/pilot.py render START END OUTDIR   -> renders frames START..END (12 fps, 640x360)
Free tools only (Blender bpy)."""
import bpy, math, sys, random
from mathutils import Vector, Matrix, Euler
FPS, TOTAL = 12, 288
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = FPS; sc.frame_start, sc.frame_end = 1, TOTAL

def mat(n, rgb, r=.5, trans=0):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = r; return m
def prim(kind, n, loc, s, m, rot=(0, 0, 0)):
    if kind == "s": bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, location=loc)
    elif kind == "c": bpy.ops.mesh.primitive_cylinder_add(vertices=40, location=loc)
    else: bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = n; o.scale = s; o.rotation_euler = rot
    if kind != "b": bpy.ops.object.shade_smooth()
    o.data.materials.append(m)
    if kind in "cb": bv = o.modifiers.new("b", "BEVEL"); bv.width = .05; bv.segments = 3
    return o

# ---------------- MODEL (real mesh parts, world-space rest pose, facing +X) ----------------
SK, KU, CAP, TR, SH, HR = mat("skin", (.78, .52, .36)), mat("kurta", (.1, .72, .4), .6), mat("cap", (.98, .97, .95), .7), mat("tr", (.96, .92, .8), .6), mat("shoe", (.45, .28, .18), .4), mat("hair", (.18, .1, .07), .6)
W_, D_, PK, MO = mat("w", (1, 1, 1), .15), mat("d", (.02, .03, .06), .1), mat("pk", (1, .5, .55)), mat("mo", (.55, .08, .12), .3)
parts = {"spine": [], "head": [], "armL": [], "armR": [], "legL": [], "legR": []}
parts["spine"] += [prim("s", "torso", (0, 0, 1.55), (.62, .5, .7), KU), prim("c", "hem", (0, 0, 1.05), (.7, .56, .12), mat("trim", (.95, .95, .9)))]
H = Vector((0, 0, 2.55))
def hp(kind, n, loc, s, m): parts["head"].append(prim(kind, n, H + Vector(loc), s, m))
hp("s", "head", (0, 0, .6), (1.2, 1.1, 1.05), SK); hp("s", "hair", (-.12, 0, .9), (1.17, 1.08, .86), HR); hp("s", "cap", (0, 0, 1.0), (1.05, 1.0, .7), CAP)
hp("s", "nose", (1.2, 0, .52), (.08, .07, .07), SK)
eyes = []; brows = []
for s in (-1, 1):
    e = prim("s", "eye", H + Vector((1.08, s * .42, .7)), (.27, .23, .33), W_); parts["head"].append(e); eyes.append(e)
    hp("s", "pupil", (1.28, s * .42, .7), (.17, .14, .25), D_); hp("s", "shine", (1.38, s * .38, .8), (.06, .06, .08), W_)
    hp("s", "cheek", (1.1, s * .66, .46), (.1, .05, .08), PK); hp("s", "ear", (-.02, s * 1.1, .55), (.16, .1, .24), SK)
    b = prim("s", "brow", H + Vector((1.12, s * .42, 1.02)), (.1, .24, .045), HR); parts["head"].append(b); brows.append(b)
mouth = prim("s", "mouth", H + Vector((1.14, 0, .34)), (.12, .3, .1), MO); parts["head"].append(mouth)
for s, k in ((-1, "R"), (1, "L")):
    parts["arm" + k] += [prim("s", "j", (0, s * .44, 2.08), (.2, .2, .2), KU), prim("c", "a", (0, s * .44, 1.74), (.2, .2, .36), KU), prim("s", "hd", (0, s * .44, 1.32), (.21, .21, .21), SK)]
    parts["leg" + k] += [prim("c", "lg", (0, s * .3, .5), (.25, .25, .46), TR), prim("s", "sho", (.1, s * .3, .08), (.32, .23, .17), SH)]

# ---------------- RIG (real armature) ----------------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0)); arm = bpy.context.object; arm.name = "Ali_rig"; arm.data.name = "Ali_rig"
eb = arm.data.edit_bones
for b in list(eb): eb.remove(b)
def bone(n, h, t, parent=None):
    b = eb.new(n); b.head, b.tail = h, t
    if parent: b.parent = eb[parent]
    return b
bone("hips", (0, 0, 1.0), (0, 0, 1.4)); bone("spine", (0, 0, 1.4), (0, 0, 2.3), "hips"); bone("head", (0, 0, 2.3), (0, 0, 3.6), "spine")
for s, k in ((1, "L"), (-1, "R")):
    bone("armL" if k == "L" else "armR", (0, s * .44, 2.08), (0, s * .44, 1.3), "spine")
    bone("legL" if k == "L" else "legR", (0, s * .3, 1.0), (0, s * .3, .1), "hips")
bpy.ops.object.mode_set(mode="OBJECT")
bpy.context.view_layer.update()
for bn, lst in parts.items():
    for o in lst:
        o.parent = arm; o.parent_type = "BONE"; o.parent_bone = bn
        o.matrix_parent_inverse = (arm.matrix_world @ arm.pose.bones[bn].matrix).inverted()
        o.matrix_world = o.matrix_world  # keep
bpy.context.view_layer.update()
mover = bpy.data.objects.new("mover", None); sc.collection.objects.link(mover); arm.parent = mover
bpy.context.view_layer.objects.active = arm
for pb in arm.pose.bones: pb.rotation_mode = "QUATERNION"

def R(bone_name, axis, deg):
    """rotation about a WORLD axis, expressed in the bone's rest frame"""
    pb = arm.pose.bones[bone_name]; rest = pb.bone.matrix_local.to_3x3()
    w = Matrix.Rotation(math.radians(deg), 3, axis)
    return (rest.inverted() @ w @ rest).to_quaternion()
def key(bone_name, f, axis, deg):
    pb = arm.pose.bones[bone_name]; pb.rotation_quaternion = R(bone_name, axis, deg); pb.keyframe_insert("rotation_quaternion", frame=f)

# ---------------- ACTION LIBRARY: idle, wave, walk, run, dance (cyclic) ----------------
def make_action(name, n, fn):
    act = bpy.data.actions.new(name); arm.animation_data_create(); arm.animation_data.action = act
    for pb in arm.pose.bones: pb.rotation_quaternion = (1, 0, 0, 0)
    for i in range(n + 1): fn(i / n * 2 * math.pi, i + 1)
    act.use_fake_user = True; arm.animation_data.action = None; return act
def idle(p, f):
    key("spine", f, "Y", 2 * math.sin(p)); key("head", f, "Y", 3 * math.sin(p + 1)); key("armL", f, "Y", -8 + 3 * math.sin(p)); key("armR", f, "Y", -8 + 3 * math.sin(p))
    key("hips", f, "Y", 0); key("legL", f, "Y", 0); key("legR", f, "Y", 0)
def wave(p, f):
    key("armL", f, "Y", 0); key("armL", f, "X", 0) if False else None
    q = R("armL", "Y", 0) ; pb = arm.pose.bones["armL"]
    pb.rotation_quaternion = (R("armL", "X", -150) @ R("armL", "Y", 0)); pb.rotation_quaternion = (R("armL", "X", 150 + 20 * math.sin(p * 4))); pb.keyframe_insert("rotation_quaternion", frame=f)
    key("armR", f, "Y", -10); key("head", f, "Y", 4 * math.sin(p)); key("spine", f, "Y", 0); key("hips", f, "Y", 0); key("legL", f, "Y", 0); key("legR", f, "Y", 0)
def walk_like(amp, bounce):
    def fn(p, f):
        key("legL", f, "Y", amp * math.sin(p)); key("legR", f, "Y", -amp * math.sin(p))
        key("armL", f, "Y", -amp * .8 * math.sin(p)); key("armR", f, "Y", amp * .8 * math.sin(p))
        key("spine", f, "Y", 4 if amp > 30 else 1); key("head", f, "Y", 2 * math.sin(2 * p)); key("hips", f, "Y", 0)
        pb = arm.pose.bones["hips"]; pb.location = (0, 0, 0); pb.keyframe_insert("location", frame=f)
        pb.location = (0, 0, bounce * abs(math.sin(p))); pb.keyframe_insert("location", frame=f)
    return fn
def dance(p, f):
    key("armL", f, "X", 110 + 45 * math.sin(p)); key("armR", f, "X", -(110 - 45 * math.sin(p)))
    key("armL", f, "X", 0) if False else None
    key("hips", f, "X", 8 * math.sin(p)); key("spine", f, "X", -6 * math.sin(p)); key("head", f, "X", 10 * math.sin(p)); key("legL", f, "Y", 10 * math.sin(2 * p)); key("legR", f, "Y", -10 * math.sin(2 * p))
    pb = arm.pose.bones["hips"]; pb.location = (0, 0, .25 * abs(math.sin(p))); pb.keyframe_insert("location", frame=f)
A = {n: make_action(n, k, fn) for n, k, fn in (("idle", 24, idle), ("wave", 12, wave), ("walk", 12, walk_like(30, .05)), ("run", 8, walk_like(50, .18)), ("dance", 12, dance))}

# ---------------- ROOM ----------------
def room():
    wall, floor, rug = mat("wall", (1, .93, .75), .8), mat("floor", (.82, .58, .36), .5), mat("rug", (.35, .7, .95), .8)
    prim("b", "floor", (0, 0, -.1), (9, 9, .1), floor); prim("b", "back", (-9, 0, 4), (.1, 9, 4.1), wall)
    prim("b", "left", (0, -9, 4), (9, .1, 4.1), mat("wl", (.8, .93, 1), .8)); prim("b", "right", (0, 9, 4), (9, .1, 4.1), mat("wr", (.8, .93, 1), .8))
    prim("c", "rug", (0, 0, .01), (4.2, 3.2, .03), rug)
    prim("b", "window", (-8.8, 0, 4.6), (.05, 2, 1.6), mat("sky", (.6, .85, 1), .05)); prim("b", "frame", (-8.85, 0, 4.6), (.04, 2.15, .08), mat("fr", (1, 1, 1)))
    prim("b", "shelf", (-8.2, -5, 1.5), (.7, 2, 1.5), mat("sf", (.95, .65, .3)))
    for i, c in enumerate(((1, .3, .3), (.2, .6, 1), (1, .85, .1), (.3, .8, .4))): prim("b", "block", (-3.5 + i * .5, 3.2, .35), (.32, .32, .32), mat(f"bk{i}", c), (0, 0, i * .4))
    prim("s", "ball", (-2, 4.2, .5), (.5, .5, .5), mat("ball", (1, .3, .45), .2))
    prim("c", "lamp", (-8, 5.5, 2.2), (.12, .12, 2.2), mat("lp", (.9, .9, .9))); prim("s", "shade", (-8, 5.5, 4.5), (.7, .7, .5), mat("sh2", (1, .9, .4), .4))
room()
for loc, e, sz in (((7, -5, 11), 650, 10), ((10, 7, 6), 220, 8)):
    bpy.ops.object.light_add(type="AREA", location=loc); l = bpy.context.object; l.data.energy = e; l.data.size = sz
    l.rotation_euler = (math.radians(60), 0, math.radians(35))
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (1, .96, .88, 1)
cam = bpy.data.cameras.new("cam"); cam.lens = 32; camo = bpy.data.objects.new("cam", cam); sc.collection.objects.link(camo); sc.camera = camo
sc.view_settings.view_transform = "Standard"

# ---------------- TIMELINE (24 s) ----------------
# 1-36 idle | 37-72 wave | 73-132 walk along room | 133-168 run | 169-288 turn, face camera and dance/sing
arm.animation_data_create(); tr = arm.animation_data.nla_tracks
def strip(name, act, start, end):
    t = tr.new(); t.name = name; s = t.strips.new(name, start, act); s.action_frame_end = act.frame_range[1]; s.action_frame_start = act.frame_range[0]
    s.frame_end = end; s.repeat = max(1.0, (end - start) / max(1, act.frame_range[1] - act.frame_range[0])); s.frame_end = end; s.influence = 1.0; s.blend_type = 'REPLACE'; s.extrapolation = 'NOTHING' if name != 'idle' else 'HOLD'; return s
for n, a0, a1 in (("idle", 1, 36), ("wave", 37, 72), ("walk", 73, 132), ("run", 133, 168), ("dance", 169, 288)): strip(n, A[n], a0, a1)
def mk(f, loc, rz):
    mover.location = loc; mover.rotation_euler = (0, 0, math.radians(rz)); mover.keyframe_insert("location", frame=f); mover.keyframe_insert("rotation_euler", frame=f)
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
mk(1, (0, -4, 0), 0); mk(60, (0, -4, 0), 0); mk(72, (0, -4, 0), 90); mk(132, (0, 0, 0), 90); mk(168, (0, 4.2, 0), 90); mk(176, (0, 4.2, 0), 90); mk(188, (0, 0, 0), 0); mk(288, (0, 0, 0), 0)
# blinking + singing mouth + brows
for f in (20, 80, 140, 200, 250):
    for e in eyes:
        for ff, v in ((f - 1, 1), (f, .1), (f + 1, 1)): e.scale = (.27, .23, .33 * v); e.keyframe_insert("scale", frame=ff)
for f in range(169, 289, 3):
    mouth.scale = (.12, .3, .05 + .12 * abs(math.sin(f * .9))); mouth.keyframe_insert("scale", frame=f)
for f in range(37, 73, 4):
    mouth.scale = (.12, .3, .06 + .08 * (f % 8 == 1)); mouth.keyframe_insert("scale", frame=f)
# camera: gentle moves
def camk(f, loc, look):
    camo.location = loc; d = Vector(look) - Vector(loc); camo.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); camo.keyframe_insert("location", frame=f); camo.keyframe_insert("rotation_euler", frame=f)
camk(1, (16, -3, 3.4), (0, -3.5, 2.2)); camk(72, (16, -2, 3.4), (0, -3, 2.2)); camk(132, (16, 0, 3.5), (0, 0, 2.2)); camk(168, (15, 2, 3.4), (0, 3, 2.2)); camk(190, (14, 0, 3.6), (0, 0, 2.3)); camk(288, (10.5, 0, 3.2), (0, 0, 2.5))

sc.render.engine = "CYCLES"; sc.cycles.use_denoising = True; sc.cycles.samples = 16
import os
if os.environ.get("DEENI_GPU") == "1":  # free GPU (e.g. Kaggle T4): CUDA/OptiX
    cp = bpy.context.preferences.addons["cycles"].preferences
    for typ in ("OPTIX", "CUDA"):
        try:
            cp.compute_device_type = typ; cp.get_devices()
            if any(d.type == typ for d in cp.devices): break
        except Exception: pass
    for d in cp.devices: d.use = d.type != "CPU"
    sc.cycles.device = "GPU"; sc.cycles.samples = int(os.environ.get("DEENI_SAMPLES", "16")); print("GPU devices:", [(d.name, d.type, d.use) for d in cp.devices], flush=True)
sc.render.resolution_x, sc.render.resolution_y = 640, 360
sc.render.use_freestyle = True; vl = sc.view_layers[0]; vl.use_freestyle = True
coll = bpy.data.collections.new("chars"); sc.collection.children.link(coll)
for o in list(sc.objects):
    if o.type == "MESH" and o.name.split(".")[0] not in ("floor", "back", "left", "right", "rug", "window", "frame", "shelf", "block", "ball", "lamp", "shade"):
        coll.objects.link(o); sc.collection.objects.unlink(o)
ls = vl.freestyle_settings.linesets.new("o"); ls.select_silhouette = ls.select_border = ls.select_crease = True; ls.select_by_collection = True; ls.collection = coll
ls.linestyle.thickness = 2.0; ls.linestyle.color = (.12, .06, .1)

if sys.argv[-1] == "save":
    bpy.ops.wm.save_as_mainfile(filepath="assets/characters/ali_pilot.blend"); print("saved .blend")
elif "render" in sys.argv:
    i = sys.argv.index("render"); a, b, out = int(sys.argv[i + 1]), int(sys.argv[i + 2]), sys.argv[i + 3]
    for f in range(a, b + 1):
        sc.frame_set(f); sc.render.filepath = f"{out}/f{f:04d}.png"; bpy.ops.render.render(write_still=True)
