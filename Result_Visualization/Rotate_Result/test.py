from __future__ import absolute_import, division, print_function, unicode_literals

import os
import tempfile
import webbrowser

import scipy.io as sio
import plotly.graph_objects as go
import numpy as np
import warnings

# Suppress .mat file loading warnings
warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

# === USER SETTINGS: Rotation Angles for subtitle ===
rx, ry, rz = 0, 0, 0

# === USER SETTINGS: Line Widths ===
lw_orig = 6  # thickness for original trajectories
lw_pred = 4    # thickness (if using lines) for predicted trajectories

# === USER SETTINGS: Marker Style for Predictions ===
pred_symbol = 'diamond'
pred_symbol_size = 0.5

# === USER SETTINGS: Colors ===
# Originals
color_0    = '#1a5276'  # 0° original
color_45   = '#1a5276'    # 45° original
color_90   = '#1a5276'  # 90° original
# Predicted (lighter variants)

color_p0   = '#DE3163'  # 0° predicted
color_p45  = '#DE3163'     # 45° predicted
color_p90  = '#DE3163'    # 90° predicted
# Base marker
base_marker_color = 'black'
base_marker_size  = 15

# -----------------------------------------------------------------------------
# Helper to load and scale XYZ from a .mat
# -----------------------------------------------------------------------------
def load_xyz(matfile, keys):
    d = sio.loadmat(matfile)
    return tuple(d[k].squeeze() * 1000 for k in keys)

# -----------------------------------------------------------------------------
# 1. Load rotated positions (org + pred) for 0°, 45°, 90°
# -----------------------------------------------------------------------------
x0,  y0,  z0   = load_xyz('TEE_Zero_org_pos_matlab.mat',     ['x_total','y_total','z_total'])
xp0, yp0, zp0 = load_xyz('TEE_Zero_predict_pos_matlab.mat', ['xp_total','yp_total','zp_total'])

x45,  y45,  z45   = load_xyz('TEE_45_org_pos_matlab.mat',     ['x_total','y_total','z_total'])
xp45, yp45, zp45 = load_xyz('TEE_45_predict_pos_matlab.mat', ['xp_total','yp_total','zp_total'])

x90,  y90,  z90   = load_xyz('TEE_90_org_pos_matlab.mat',     ['x_total','y_total','z_total'])
xp90, yp90, zp90 = load_xyz('TEE_90_predict_pos_matlab.mat', ['xp_total','yp_total','zp_total'])

# -----------------------------------------------------------------------------
# 2. Build 3D plot (solid lines for originals, symbols for predictions)
# -----------------------------------------------------------------------------
fig = go.Figure()

# Original trajectories (solid lines)
for x,y,z,name,color in [
    (x0, y0, z0, 'Original 0°', color_0),
    (x45, y45, z45, 'Original 45°', color_45),
    (x90, y90, z90, 'Original 90°', color_90)
]:
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color=color, width=lw_orig),
        name=name
    ))

# Predicted trajectories (lines with markers)
for xp,yp,zp,name,color in [
    (xp0, yp0, zp0, 'Predicted 0°', color_p0),
    (xp45, yp45, zp45, 'Predicted 45°', color_p45),
    (xp90, yp90, zp90, 'Predicted 90°', color_p90)
]:
    fig.add_trace(go.Scatter3d(
        x=xp, y=yp, z=zp,
        mode='lines+markers',
        line=dict(color=color, width=lw_pred),
        marker=dict(symbol=pred_symbol, size=pred_symbol_size, color=color),
        name=name
    ))

# --- Base Marker at the Origin ---
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=base_marker_size, color=base_marker_color, symbol='circle'),
    name='Origin'
))

# -----------------------------------------------------------------------------
# 3. Layout styling (template)
# -----------------------------------------------------------------------------
fig.update_layout(
    title=dict(
        text=f"<b>Original vs. Predicted Trajectories</b><br>"
             f"<span style='font-size:12px'>Rotated X={rx}°, Y={ry}°, Z={rz}°</span>",
        font=dict(size=20), x=0.5
    ),
    scene=dict(
        xaxis=dict(title=dict(text='X (mm)', font=dict(size=16)),
                   tickfont=dict(size=12), gridcolor='lightgray', zerolinecolor='gray',
                   showbackground=True, backgroundcolor='white'),
        yaxis=dict(title=dict(text='Y (mm)', font=dict(size=16)),
                   tickfont=dict(size=12), gridcolor='lightgray', zerolinecolor='gray',
                   showbackground=True, backgroundcolor='white'),
        zaxis=dict(title=dict(text='Z (mm)', font=dict(size=16)),
                   tickfont=dict(size=12), gridcolor='lightgray', zerolinecolor='gray',
                   showbackground=True, backgroundcolor='white'),
        bgcolor='white', aspectmode='data'
    ),
    legend=dict(font=dict(size=14), bordercolor='white', borderwidth=1),
    margin=dict(l=10, r=10, b=10, t=80), width=1000, height=800
)

# -----------------------------------------------------------------------------
# 4. Export to HTML and open
# -----------------------------------------------------------------------------
tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
fig.write_html(tmp.name, auto_open=False)
webbrowser.open('file://' + os.path.realpath(tmp.name))
