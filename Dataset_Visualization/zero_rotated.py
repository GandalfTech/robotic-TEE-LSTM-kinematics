import scipy.io
import numpy as np
import plotly.graph_objects as go
import warnings

# Suppress .mat file loading warnings
warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

# === USER SETTINGS ===
# Rotation Angles (degrees) for rotated plot
rx, ry, rz = 0, -20, 40

# Line Width
line_width = 8

# Colors
color_original = '#85c1e9'
color_rotated  = 'blue'

# Base Marker
base_marker_color  = 'black'
base_marker_size   = 30
base_marker_symbol = 'circle'

# Figure Size & Data Slice
window_width, window_height = 1600, 1000
start_index, end_index = None, None   # slice your data if needed

# Scene Styling
scene_bgcolor         = '#ffffff'
scene_axis_line_color = 'gray'

# Axis Text Styling
axis_title_bold   = True
axis_title_size   = 14
axis_tick_size    = 12
axis_font_family  = 'Arial'

# === Helper Functions ===
def rotation_matrix(rx, ry, rz):
    rx, ry, rz = np.radians([rx, ry, rz])
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rx), -np.sin(rx)],
                   [0, np.sin(rx),  np.cos(rx)]])
    Ry = np.array([[np.cos(ry), 0, np.sin(ry)],
                   [0, 1, 0],
                   [-np.sin(ry), 0, np.cos(ry)]])
    Rz = np.array([[np.cos(rz), -np.sin(rz), 0],
                   [np.sin(rz),  np.cos(rz), 0],
                   [0, 0, 1]])
    return Rz @ Ry @ Rx

# Format axis titles
def fmt_title(text):
    return f"<b>{text}</b>" if axis_title_bold else text

# === Load Data ===
data_zero = scipy.io.loadmat("Robot_Data_Zero.mat")
ir1 = data_zero['ir_positions']
ir2 = data_zero['ir_positions2']
rel = ir1 - ir2
# reorder axes [x, z, -y] and convert to mm
rel_mm = np.vstack([rel[0], rel[2], -rel[1]]) * 1000

# Apply rotation
R = rotation_matrix(rx, ry, rz)
rotated_mm = R @ rel_mm

# Optionally slice
orig_x, orig_y, orig_z = rel_mm[:, start_index:end_index]
rot_x, rot_y, rot_z    = rotated_mm[:, start_index:end_index]

# === Plot ===
fig = go.Figure()

# Original Trajectory
fig.add_trace(go.Scatter3d(
    x=orig_x, y=orig_y, z=orig_z,
    mode='lines',
    line=dict(color=color_original, width=line_width),
    name='Original'
))

# Rotated Trajectory
fig.add_trace(go.Scatter3d(
    x=rot_x, y=rot_y, z=rot_z,
    mode='lines',
    line=dict(color=color_rotated, width=line_width),
    name=f'Rotated (X={rx}°, Y={ry}°, Z={rz}°)'
))

# Base Marker
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=base_marker_size, color=base_marker_color, symbol=base_marker_symbol),
    name='Base'
))

# Layout
fig.update_layout(
    title=dict(
        text='<b>Original vs Rotated Zero Dataset</b>',
        font=dict(size=20), x=0.5
    ),
    scene=dict(
        xaxis=dict(
            title=dict(text=fmt_title('X (mm)'), font=dict(size=axis_title_size, family=axis_font_family)),
            tickfont=dict(size=axis_tick_size, family=axis_font_family),
            gridcolor=scene_axis_line_color,
            zerolinecolor=scene_axis_line_color,
            backgroundcolor=scene_bgcolor
        ),
        yaxis=dict(
            title=dict(text=fmt_title('Y (mm)'), font=dict(size=axis_title_size, family=axis_font_family)),
            tickfont=dict(size=axis_tick_size, family=axis_font_family),
            gridcolor=scene_axis_line_color,
            zerolinecolor=scene_axis_line_color,
            backgroundcolor=scene_bgcolor
        ),
        zaxis=dict(
            title=dict(text=fmt_title('Z (mm)'), font=dict(size=axis_title_size, family=axis_font_family)),
            tickfont=dict(size=axis_tick_size, family=axis_font_family),
            gridcolor=scene_axis_line_color,
            zerolinecolor=scene_axis_line_color,
            backgroundcolor=scene_bgcolor
        ),
        bgcolor=scene_bgcolor
    ),
    width=window_width,
    height=window_height,
    margin=dict(l=10, r=10, b=10, t=50)
)

fig.show()
