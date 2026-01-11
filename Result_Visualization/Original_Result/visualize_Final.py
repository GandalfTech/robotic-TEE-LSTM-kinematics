from __future__ import absolute_import, division, print_function, unicode_literals

import os
import tempfile
import webbrowser

import scipy.io as sio
import plotly.graph_objects as go

# === USER SETTINGS: Rotation Angles for subtitle ===
rx, ry, rz = 0, -20, 40

# === USER SETTINGS: Line Widths ===
lw_orig = 6    # thickness for original trajectories
lw_pred = 3    # thickness for predicted trajectories

# === USER SETTINGS: Colors ===
# Originals
color_0    = '#1b4f72'   # 0° original
color_45   = '#212f3c'   # 45° original
color_90   = '#196f3d'   # 90° original
# Predicted (lighter variants)
color_p0   = 'red'   # 0° predicted
color_p45  = 'red'   # 45° predicted
color_p90  = 'red'   # 90° predicted
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
x0,  y0,  z0   = load_xyz('TEE_zero_org_pos_matlab_rotate.mat',     ['x_total_zero','y_total_zero','z_total_zero'])
xp0, yp0, zp0 = load_xyz('TEE_zero_predict_pos_matlab_rotate.mat', ['xp_total_zero','yp_total_zero','zp_total_zero'])

x45,  y45,  z45   = load_xyz('TEE_45_org_pos_matlab_rotate.mat',     ['x_total_45','y_total_45','z_total_45'])
xp45, yp45, zp45 = load_xyz('TEE_45_predict_pos_matlab_rotate.mat', ['xp_total_45','yp_total_45','zp_total_45'])

x90,  y90,  z90   = load_xyz('TEE_90_org_pos_matlab_rotate.mat',     ['x_total_90','y_total_90','z_total_90'])
xp90, yp90, zp90 = load_xyz('TEE_90_predict_pos_matlab_rotate.mat', ['xp_total_90','yp_total_90','zp_total_90'])

# -----------------------------------------------------------------------------
# 2. Build 3D line plot (solid for both original & predicted)
# -----------------------------------------------------------------------------
fig = go.Figure()

# Original trajectories
fig.add_trace(go.Scatter3d(
    x=x0, y=y0, z=z0,
    mode='lines',
    line=dict(color=color_0, width=lw_orig),
    name='Original 0°'
))
fig.add_trace(go.Scatter3d(
    x=x45, y=y45, z=z45,
    mode='lines',
    line=dict(color=color_45, width=lw_orig),
    name='Original 45°'
))
fig.add_trace(go.Scatter3d(
    x=x90, y=y90, z=z90,
    mode='lines',
    line=dict(color=color_90, width=lw_orig),
    name='Original 90°'
))

# Predicted trajectories
fig.add_trace(go.Scatter3d(
    x=xp0, y=yp0, z=zp0,
    mode='lines',
    line=dict(color=color_p0, width=lw_pred),
    name='Predicted 0°'
))
fig.add_trace(go.Scatter3d(
    x=xp45, y=yp45, z=zp45,
    mode='lines',
    line=dict(color=color_p45, width=lw_pred),
    name='Predicted 45°'
))
fig.add_trace(go.Scatter3d(
    x=xp90, y=yp90, z=zp90,
    mode='lines',
    line=dict(color=color_p90, width=lw_pred),
    name='Predicted 90°'
))

# --- Base Marker at the Origin ---
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=base_marker_size, color=base_marker_color, symbol='circle'),
    name='Origin'
))

# -----------------------------------------------------------------------------
# 3. Layout styling (your template)
# -----------------------------------------------------------------------------
fig.update_layout(
    title=dict(
        text=f"<b>Original vs. Predicted Trajectories</b><br>"
             f"<span style='font-size:12px'>Rotated X={rx}°, Y={ry}°, Z={rz}°</span>",
        font=dict(size=20), x=0.5
    ),
    scene=dict(
        xaxis=dict(title=dict(text='X (mm)', font=dict(size=16)),
                   tickfont=dict(size=12),
                   gridcolor='lightgray',
                   zerolinecolor='gray',
                   showbackground=True,
                   backgroundcolor='white'),
        yaxis=dict(title=dict(text='Y (mm)', font=dict(size=16)),
                   tickfont=dict(size=12),
                   gridcolor='lightgray',
                   zerolinecolor='gray',
                   showbackground=True,
                   backgroundcolor='white'),
        zaxis=dict(title=dict(text='Z (mm)', font=dict(size=16)),
                   tickfont=dict(size=12),
                   gridcolor='lightgray',
                   zerolinecolor='gray',
                   showbackground=True,
                   backgroundcolor='white'),
        bgcolor='white',
        aspectmode='data'
    ),
    legend=dict(font=dict(size=14), bordercolor='white', borderwidth=1),
    margin=dict(l=10, r=10, b=10, t=80),
    width=1000,
    height=800
)

# -----------------------------------------------------------------------------
# 4. Export to HTML and open
# -----------------------------------------------------------------------------
tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
fig.write_html(tmp.name, auto_open=False)
webbrowser.open('file://' + os.path.realpath(tmp.name))
