# DEENIKIDS 3D pilot (free tools only)
Install: `pip install bpy` (Blender as a Python module, Python 3.11+). Run:
- `python blender/pilot.py save` writes `assets/characters/ali_pilot.blend` (editable rigged model, 5 actions, room).
- `python blender/pilot.py render 1 288 out_dir` renders frames at 12 fps, 640x360; assemble with `ffmpeg -framerate 12 -i out_dir/f%04d.png -c:v libx264 -pix_fmt yuv420p pilot.mp4`.
Measured (2 free CPU cores): about 12 seconds per frame, so a 24 s pilot took about 58 minutes.
## Status
Done: Ali mesh, rig (hips/spine/head/arms/legs), actions idle, wave, walk, run, dance, room, blinking, talking mouth, 24 s pilot.
Limits: rigid parts (no bending elbows/knees, no fingers), no IK, no lip-sync from audio yet, no sound in the pilot, 640x360 only.
