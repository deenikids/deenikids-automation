"""PHASE 1 pilot: Ali (toddler boy) as a 3D character, built from code in Blender (free). Usage: python blender/ali3d.py SAMPLES out.png [wave]"""
import bpy, math, sys, time
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
def mat(n, rgb, r=0.45, sss=0.0):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = r
    if sss: b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Subsurface Radius"].default_value = (1, .4, .3)
    return m
def part(kind, n, loc, sc_, m, parent=None, rot=(0, 0, 0)):
    if kind == "s": bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, location=loc)
    elif kind == "c": bpy.ops.mesh.primitive_cylinder_add(vertices=48, location=loc)
    o = bpy.context.object; o.name = n; o.scale = sc_; o.rotation_euler = rot
    bpy.ops.object.shade_smooth(); o.data.materials.append(m)
    if kind == "c":
        bev = o.modifiers.new("b", "BEVEL"); bev.width = 0.06; bev.segments = 4
    if parent: o.parent = parent; o.location = loc  # loc is local to the parent pivot
    return o
def pivot(n, loc, parent=None):
    e = bpy.data.objects.new(n, None); sc.collection.objects.link(e); e.location = loc
    if parent: e.parent = parent
    return e
skin, kurta, cap, trouser, shoe, hair, white, dark, pink = (mat("skin", (.78, .52, .36), .5, .15), mat("kurta", (.12, .62, .35), .6), mat("cap", (.98, .97, .95), .7),
    mat("tr", (.96, .92, .8), .6), mat("shoe", (.45, .28, .18), .4), mat("hair", (.18, .1, .07), .6), mat("w", (1, 1, 1), .15), mat("d", (.02, .03, .06), .1), mat("p", (1, .5, .55), .5))
root = pivot("ali", (0, 0, 0))
body = part("s", "torso", (0, 0, 1.55), (.62, .5, .82), kurta, root)
part("c", "hem", (0, 0, 1.05), (.7, .56, .12), mat("trim", (.95, .95, .9), .5), root)
head = pivot("headp", (0, 0, 2.55), root)
part("s", "head", (0, 0, .55), (.95, .88, .88), skin, head)
part("s", "hair", (-.12, 0, .78), (.93, .86, .7), hair, head)
part("s", "cap", (0, 0, .86), (.82, .76, .62), cap, head)
part("c", "capband", (0, 0, .5), (.0, .0, .0), mat("band", (.9, .9, .88), .6), head)
for s in (-1, 1):
    part("s", "ear", (-.02, s * .92, .52), (.14, .08, .2), skin, head)
    part("s", "eyew", (.78, s * .33, .62), (.19, .17, .24), white, head)
    part("s", "pupil", (.94, s * .33, .62), (.1, .09, .16), dark, head)
    part("s", "shine", (1.02, s * .3, .7), (.035, .035, .05), white, head)
    part("s", "cheek", (.8, s * .56, .38), (.1, .05, .08), pink, head)
    part("s", "brow", (.88, s * .33, .9), (.09, .2, .04), hair, head, (0, 0, 0))
part("s", "nose", (.9, 0, .5), (.08, .07, .07), skin, head)
part("s", "mouth", (.86, 0, .3), (.1, .16, .06), mat("mouth", (.55, .08, .12), .3), head)
part("s", "tongue", (.9, 0, .27), (.05, .09, .03), pink, head)
arms = {}
for s, nm in ((-1, "R"), (1, "L")):
    sh = pivot("sh" + nm, (0, s * .6, 2.05), root)
    part("c", "arm", (0, 0, -.34), (.17, .17, .4), kurta, sh)
    part("s", "hand", (0, 0, -.76), (.17, .17, .17), skin, sh)
    arms[nm] = sh
    lg = pivot("lg" + nm, (0, s * .3, 1.0), root)
    part("c", "leg", (0, 0, -.5), (.2, .2, .5), trouser, lg)
    part("s", "shoe", (.1, 0, -.92), (.32, .23, .17), shoe, lg)
# pose: arms
arms["R"].rotation_euler = (math.radians(-25), 0, 0)
if "wave" in sys.argv: arms["L"].rotation_euler = (math.radians(145), 0, 0)
else: arms["L"].rotation_euler = (math.radians(25), 0, 0)
head.rotation_euler = (0, 0, math.radians(-8))
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0)); bpy.context.object.data.materials.append(mat("floor", (.95, .72, .42), .7))
bpy.ops.object.light_add(type='AREA', location=(5, -4, 7)); L = bpy.context.object; L.data.energy = 450; L.data.size = 6
bpy.ops.object.light_add(type='AREA', location=(4, 5, 3)); L2 = bpy.context.object; L2.data.energy = 140; L2.data.size = 5
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.75, .88, 1, 1); bg.inputs[1].default_value = 1.0
bpy.ops.object.camera_add(location=(15, -.3, 2.0), rotation=(math.radians(88), 0, math.radians(90))); sc.camera = bpy.context.object; sc.camera.data.lens = 50
sc.view_settings.view_transform = "Standard"; sc.render.engine = "CYCLES"; sc.cycles.samples = int(sys.argv[-3] if "wave" in sys.argv else sys.argv[-2]); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 960, 540
sc.render.filepath = [a for a in sys.argv if a.endswith(".png")][0]
t0 = time.time(); bpy.ops.render.render(write_still=True); print("RENDER SECONDS", round(time.time() - t0, 1))
