"""Free 3D test: build Deeni (blue baby shark in a bubble) procedurally in Blender and render one frame."""
import bpy, math, sys, time
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, rgb, rough=0.35):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    return m

def sphere(name, loc, scale, m, seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg//2, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.shade_smooth(); o.data.materials.append(m); return o

blue, belly, white, dark, pink = mat("blue",(0.08,0.45,0.85)), mat("belly",(1,0.93,0.78)), mat("w",(1,1,1),0.2), mat("d",(0.03,0.04,0.08),0.1), mat("p",(1,0.55,0.65))
body = sphere("body", (0,0,0), (1.25,0.9,0.95), blue)
sphere("belly", (0.1,-0.35,-0.25), (1.0,0.62,0.6), belly)
for s in (-1,1):
    sphere("eyew", (0.95,s*0.42,0.3), (0.26,0.2,0.28), white)
    sphere("pupil", (1.14,s*0.42,0.3), (0.14,0.11,0.17), dark)
    sphere("cheek", (0.95,s*0.62,-0.05), (0.14,0.06,0.1), pink)
# tail, fin
bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.55, depth=0.12, location=(0,0,1.0), rotation=(0,0,0)); fin=bpy.context.object; fin.data.materials.append(blue); fin.scale=(1,0.3,1.2)
bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.5, depth=0.12, location=(-1.45,0,0.1), rotation=(0,math.radians(-90),0)); t=bpy.context.object; t.data.materials.append(blue)
# bubble
bub = sphere("bubble", (0,0,0), (2.0,2.0,2.0), mat("bub",(0.8,0.95,1)))
bm = bub.data.materials[0]; b = bm.node_tree.nodes["Principled BSDF"]
b.inputs["Transmission Weight"].default_value = 1.0; b.inputs["Roughness"].default_value = 0.02; b.inputs["Alpha"].default_value = 0.3
# floor, light, camera
bpy.ops.mesh.primitive_plane_add(size=30, location=(0,0,-2.1)); bpy.context.object.data.materials.append(mat("floor",(1,0.85,0.55),0.6))
bpy.ops.object.light_add(type='AREA', location=(3,-4,6)); L=bpy.context.object; L.data.energy=900; L.data.size=6
sc.world = bpy.data.worlds.new("w"); sc.world.use_nodes=True; sc.world.node_tree.nodes["Background"].inputs[0].default_value=(1,0.95,0.85,1); sc.world.node_tree.nodes["Background"].inputs[1].default_value=1.2
bpy.ops.object.camera_add(location=(6.5,-0.6,0.8), rotation=(math.radians(88),0,math.radians(90))); sc.camera=bpy.context.object
sc.render.engine = 'CYCLES'; sc.cycles.samples = int(sys.argv[-2]); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 960, 540
sc.render.filepath = sys.argv[-1]
t0=time.time(); bpy.ops.render.render(write_still=True); print("RENDER SECONDS", round(time.time()-t0,1))
