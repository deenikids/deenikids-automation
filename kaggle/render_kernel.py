"""Kaggle free-GPU speed test for the DEENIKIDS 3D pilot (runs on Kaggle, not locally)."""
import os, subprocess, sys, time, urllib.request, glob, shutil
def sh(c): print("+", c, flush=True); r = subprocess.run(c, shell=True, capture_output=True, text=True); print(r.stdout[-1500:], r.stderr[-1500:], flush=True); return r
sh("nvidia-smi -L"); print(sys.version, flush=True)
sh("pip install -q bpy 2>&1 | tail -3")
os.makedirs("/tmp/w/blender", exist_ok=True); os.chdir("/tmp/w")
urllib.request.urlretrieve("https://raw.githubusercontent.com/deenikids/deenikids-automation/main/blender/pilot.py", "blender/pilot.py")
os.makedirs("/tmp/w/assets/characters", exist_ok=True); os.makedirs("/kaggle/working/frames", exist_ok=True)
env = dict(os.environ, DEENI_GPU="1")
for res in ((640, 360, 16),):
    t0 = time.time()
    r = subprocess.run([sys.executable, "blender/pilot.py", "render", "100", "112", "/kaggle/working/frames"], env=env, capture_output=True, text=True)
    print(r.stdout[-2500:], r.stderr[-2500:], flush=True)
    n = len(glob.glob("/kaggle/working/frames/*.png")); dt = time.time() - t0
    print(f"RESULT frames={n} seconds={dt:.1f} sec_per_frame={dt / max(1, n):.2f}", flush=True)
