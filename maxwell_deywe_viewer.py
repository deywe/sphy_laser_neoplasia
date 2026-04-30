from ursina import *
import pandas as pd
import numpy as np
import hashlib
import sys

app = Ursina()
window.title = "MAXWELL-DEYWE QUANTUM SURGERY INTERFACE - SPHY-MED"
window.color = color.black

# 1. System Loading and Data Manifold Initialization
print("🚀 Loading Quantum Phase Manifold...")
try:
    # Loading the medical simulation data
    df = pd.read_parquet("laser_medico_quantum.parquet")
    unique_frames = df['frame'].unique()
    
    # Pre-ordering frames to ensure real-time performance and hash parity
    frames = [df[df['frame'] == f].sort_values(['x', 'y']) for f in unique_frames]
    grid_size = int(np.sqrt(len(frames[0])))
    
    print(f"✅ Manifold Ready. Grid Resolution: {grid_size}x{grid_size}")
    print(f"📊 Total Forensic Frames: {len(unique_frames)}")
except Exception as e:
    print(f"❌ Error loading Data Manifold: {e}")
    sys.exit()

# 2. Biological Tissue / Neoplasm Mesh Setup
# X and Y represent the spatial manifold; Z represents the Phase Pressure Gradient
terrain = Entity(model=Mesh(
    vertices=[Vec3(0,0,0) for _ in range(grid_size**2)],
    triangles=[(i, i+1, i+grid_size) for x in range(grid_size-1) for y in range(grid_size-1) for i in [x*grid_size+y] for _ in [0]] +
              [(i+1, i+grid_size+1, i+grid_size) for x in range(grid_size-1) for y in range(grid_size-1) for i in [x*grid_size+y] for _ in [0]],
    mode='triangle'
), double_sided=True)

# 3. Medical HUD (Heads-Up Display)
title_txt = Text(text="MODE: PHASE-TUNNELING SURGERY", position=(-0.85, 0.45), color=color.red, scale=1.2)
integrity_txt = Text(text="SHA-256: INITIALIZING VALIDATION", position=(-0.85, 0.40), scale=0.8)
target_txt = Text(text="TARGET: NEOPLASM IDENTIFIED", position=(-0.85, 0.35), color=color.green, scale=0.8)
frame_txt = Text(text="FRAME: 0", position=(-0.85, 0.30), color=color.gray, scale=0.8)

idx = 0

def update():
    global idx
    current_data = frames[idx]
    
    # Vectorized extraction for GPU performance
    zs = current_data['z'].values
    xs = current_data['x'].values
    ys = current_data['y'].values
    
    # Update vertices (Mapping SPHY Z-Pressure to Ursina Y-Axis)
    terrain.model.vertices = [Vec3(xs[i], zs[i], ys[i]) for i in range(len(zs))]
    
    # Adaptive Coloration: 
    # Green = Stable Biological Tissue | Red = Quantum Phase Collapse (Target Ablation)
    terrain.model.colors = [color.rgb(255*clamp(z, 0, 1), 255*(1-clamp(z, 0, 1)), 50) for z in zs]
    
    # 4. SHA-256 Forensic Integrity Validation (Harpia Protocol)
    # Reconstructing the phase string with 6-decimal precision
    check_content = "".join(
        current_data['x'].map('{:.6f}'.format) + 
        current_data['y'].map('{:.6f}'.format) + 
        current_data['z'].map('{:.6f}'.format)
    )
    
    calc_hash = hashlib.sha256(check_content.encode('utf-8')).hexdigest()
    stored_hash = current_data['sha256_signature'].iloc[0]
    
    if calc_hash == stored_hash:
        integrity_txt.text = f"INTEGRITY: SECURE ({calc_hash[:12]})"
        integrity_txt.color = color.green
    else:
        integrity_txt.text = "!!! CRITICAL: LASER PHASE BREACH !!!"
        integrity_txt.color = color.red
        # In a real SPHY-MED device, this would trigger an immediate beam shutdown.

    terrain.model.generate()
    frame_txt.text = f"FRAME: {idx}"
    
    # Loop the simulation manifold
    idx = (idx + 1) % len(frames)

EditorCamera() # Allows rotation (RMB) and movement (WASD)
app.run()
