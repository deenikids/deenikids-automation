"""All four DEENIKIDS characters in 3D (code-built, free). Usage: python blender/lineup3d.py SAMPLES out.png"""
import bpy, math, sys
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
def mat(n, rgb, r=.45, sss=0.0):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = r
    if sss: b.inputs["Subsurface Weight"].default_value = sss
    return m
def part(kind, n, loc, s, m, parent=None):
    if kind == "s": bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24)
    else:
        bpy.ops.mesh.primitive_cylinder_add(vertices=48)
    o = bpy.context.object; o.name = n; o.scale = s
    bpy.ops.object.shade_smooth(); o.data.materials.append(m)
    if kind == "c": b = o.modifiers.new("b", "BEVEL"); b.width = .06; b.segments = 4
    if parent: o.parent = parent
    o.location = loc; return o
def pivot(n, loc, parent=None):
    e = bpy.data.objects.new(n, None); sc.collection.objects.link(e); e.location = loc
    if parent: e.parent = parent
    return e
W, D, PINK, MOUTH = mat("w", (1, 1, 1), .15), mat("d", (.02, .03, .06), .1), mat("pk", (1, .5, .55), .5), mat("mo", (.55, .08, .12), .3)
def face(head, y0=1.08, z=.7, wide=.42, hood=False):
    for s in (-1, 1):
        part("s", "ew", (y0, s * wide, z), (.27, .23, .33), W, head)
        part("s", "pu", (y0 + .2, s * wide, z), (.17, .14, .25), D, head)
        part("s", "sh", (y0 + .3, s * (wide - .04), z + .1), (.06, .06, .08), W, head)
        part("s", "ch", (y0 + .02, s * .56, z - .24), (.1, .05, .08), PINK, head)
    part("s", "mo", (y0 + .06, 0, z - .36), (.12, .3, .1), MOUTH, head)
def child(x, skin_rgb, outfit, trouser, shoe, hijab=None, taqiyah=False, dress=False):
    root = pivot("c", (0, x, 0)); skin = mat("sk", skin_rgb, .5, .15); out = mat("o", outfit, .6)
    part("s", "torso", (0, 0, 1.55), (.62, .5, .7), out, root)
    if dress: part("c", "skirt", (0, 0, 1.05), (.82, .66, .42), out, root)
    else: part("c", "hem", (0, 0, 1.05), (.7, .56, .12), mat("t", (.95, .95, .9), .5), root)
    head = pivot("h", (0, 0, 2.55), root)
    part("s", "head", (0, 0, .6), (1.2, 1.1, 1.05), skin, head)
    face(head)
    part("s", "nose", (1.2, 0, .52), (.08, .07, .07), skin, head)
    if hijab:  # hijab wraps hair, ears and neck; face stays open
        hj = mat("hj", hijab, .55)
        part("s", "hj", (-.15, 0, .66), (1.3, 1.26, 1.22), hj, head)
        part("s", "hjn", (0, 0, -.2), (.95, .9, .32), hj, head)
        part("s", "frame", (.32, 0, .6), (1.0, .92, .9), skin, head)  # re-expose face
        face(head)
    elif taqiyah:
        part("s", "hair", (-.12, 0, .9), (1.17, 1.08, .86), mat("hr", (.18, .1, .07), .6), head)
        part("s", "cap", (0, 0, 1.0), (1.05, 1.0, .7), mat("cp", (.98, .97, .95), .7), head)
        for s in (-1, 1): part("s", "ear", (-.02, s * 1.1, .55), (.16, .1, .24), skin, head)
    for s in (-1, 1):
        sh = pivot("s", (0, s * .44, 2.08), root)
        part("s", "j", (0, 0, 0), (.2, .2, .2), out, sh); part("c", "a", (0, 0, -.34), (.2, .2, .36), out, sh); part("s", "hd", (0, 0, -.76), (.21, .21, .21), skin, sh)
        sh.rotation_euler = (math.radians(s * 25 + (95 if (s == 1 and hijab) else 0)), 0, 0)
        lg = pivot("l", (0, s * .3, 1.0), root)
        part("c", "lg", (0, 0, -.5), (.25, .25, .46), trouser, lg); part("s", "sho", (.1, 0, -.92), (.32, .23, .17), shoe, lg)
    return root
c_ali = child(-2.6, (.78, .52, .36), (.1, .72, .4), mat("tr", (.96, .92, .8), .6), mat("sh", (.45, .28, .18), .4), taqiyah=True)
c_mina = child(-.9, (.8, .55, .4), (.98, .55, .72), mat("tm", (.98, .55, .72), .6), mat("sm", (.6, .25, .45), .4), hijab=(.95, .42, .62), dress=True)
# Bubbles the octopus
ob = pivot("bub", (0, 1.0, 0)); yel = mat("y", (1, .82, .15), .4, .2); ora = mat("or", (1, .55, .15), .5)
part("s", "body", (0, 0, 1.6), (1.0, .95, 1.05), yel, ob); face(ob.children[0] if False else pivot("bh", (0, 0, 1.15), ob), y0=.7, z=.55, wide=.36)
for i in range(8):
    a = i / 8 * 2 * math.pi; t = part("s", "tent", (math.cos(a) * .85, math.sin(a) * .85, .55), (.2, .2, .55), yel, ob); t.rotation_euler = (math.sin(a) * .35, -math.cos(a) * .35, 0)
for sx, sy in ((.45, .5), (.2, -.62), (-.3, .3), (.55, -.2)): part("s", "spot", (sx, sy, 2.4), (.14, .14, .1), ora, ob)
# Deeni, the baby shark in a bubble
dn = pivot("deeni", (0, 3.6, 1.8)); blue = mat("bl", (.08, .45, .85), .35); bel = mat("be", (1, .93, .78), .4)
part("s", "b", (0, 0, 0), (1.2, .85, .9), blue, dn); part("s", "be", (.12, 0, -.3), (.95, .65, .55), bel, dn)
part("s", "fin", (0, 0, .95), (.35, .08, .55), blue, dn); part("s", "tail", (-1.35, 0, .05), (.5, .1, .6), blue, dn)
dh = pivot("dh", (.4, 0, .25), dn); face(dh, y0=.62, z=0, wide=.38)
bub = part("s", "bubble", (0, 0, 0), (2.0, 1.6, 1.6), mat("bu", (.8, .95, 1), .02), dn); bp = bub.data.materials[0].node_tree.nodes["Principled BSDF"]
bp.inputs["Transmission Weight"].default_value = 1; bp.inputs["Alpha"].default_value = .25
bpy.ops.mesh.primitive_plane_add(size=60); floor = bpy.context.object; floor.data.materials.append(mat("fl", (.95, .72, .42), .7))
for loc, e, sz in (((6, -6, 9), 700, 8), ((8, 7, 4), 220, 6)):
    bpy.ops.object.light_add(type='AREA', location=loc); l = bpy.context.object; l.data.energy = e; l.data.size = sz
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.75, .88, 1, 1)
bpy.ops.object.camera_add(location=(17, .4, 2.5), rotation=(math.radians(88), 0, math.radians(90))); sc.camera = bpy.context.object; sc.camera.data.lens = 38
sc.view_settings.view_transform = "Standard"; sc.render.engine = "CYCLES"; sc.cycles.samples = int(sys.argv[-2]); sc.cycles.use_denoising = True
sc.render.use_freestyle = True; vl = sc.view_layers[0]; vl.use_freestyle = True
ls = vl.freestyle_settings.linesets.new("outline"); ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True
coll = bpy.data.collections.new("chars"); sc.collection.children.link(coll)
for o in list(sc.objects):
    if o is not floor and o.type in {"MESH"}: coll.objects.link(o); sc.collection.objects.unlink(o)
ls.select_by_collection = True; ls.collection = coll
ls.linestyle.thickness = 3.0; ls.linestyle.color = (.12, .06, .1)
sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.render.filepath = sys.argv[-1]
bpy.ops.render.render(write_still=True)
