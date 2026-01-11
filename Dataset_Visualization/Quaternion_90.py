import scipy.io
import numpy as np
import plotly.graph_objects as go
import warnings

# Suppress .mat file loading warnings
warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

# === USER SETTINGS ===
rx, ry, rz = 0, -20, 40          # global rotation (degrees)
window_width, window_height = 1800, 1100
start_index, end_index = 0, None
sample_step = 50                  # draw orientation arrows every N samples
line_width = 6
arrow_scale = 0.15
arrow_width = 2

# Marker origin styling
base_marker_size = 30            # size of the origin marker
base_marker_color = 'black'
base_marker_symbol = 'circle'

# Font settings
legend_font_family = 'Arial'
legend_font_size = 14
axis_title_font_family = 'Arial'
axis_title_font_size = 16
axis_title_bold = True            # make axis titles bold
axis_tick_font_size = 12

# Scene styling
scene_bgcolor = 'white'
scene_axis_line_color = 'gray'

# Colors
color_original = '#e74c3c'
color_traj     = '#6e2c00'
color_arrow_x  = 'red'            # X-axis in red
color_arrow_y  = 'green'          # Y-axis in green
color_arrow_z  = 'blue'         # Z-axis in violet

# === Helper: Rotation matrix ===
def rotation_matrix(rx, ry, rz):
    rx, ry, rz = np.radians([rx, ry, rz])
    Rx = np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx), np.cos(rx)]])
    Ry = np.array([[ np.cos(ry), 0, np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]])
    Rz = np.array([[ np.cos(rz), -np.sin(rz), 0],[np.sin(rz), np.cos(rz), 0],[0,0,1]])
    return Rz @ Ry @ Rx

# === Load 90° data ===
data = scipy.io.loadmat("Robot_Data_90F.mat")  # 90° dataset
ir1 = data['ir_positions']
ir2 = data['ir_positions2']
rel = ir1 - ir2            # 3×N relative marker vector
rel_mm = np.vstack([rel[0], rel[2], -rel[1]]) * 1000  # reorder & mm

# Apply global rotation
Rmat = rotation_matrix(rx, ry, rz)
rel_rot = Rmat @ rel_mm

# Slice for plotting
orig = rel_mm[:, start_index:end_index]
rot  = rel_rot[:, start_index:end_index]
orig_x, orig_y, orig_z = orig
X, Y, Z               = rot
unit_vs = (rel_rot / np.linalg.norm(rel_rot, axis=0))[:, start_index:end_index]

# Build figure
fig = go.Figure()
fig.add_trace(go.Scatter3d(
    x=orig_x, y=orig_y, z=orig_z,
    mode='lines', line=dict(color=color_original, width=line_width),
    name='Original 90° Trajectory'
))
fig.add_trace(go.Scatter3d(
    x=X, y=Y, z=Z,
    mode='lines', line=dict(color=color_traj, width=line_width),
    name='Rotated 90° Trajectory'
))
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0], mode='markers',
    marker=dict(size=base_marker_size, color=base_marker_color, symbol=base_marker_symbol),
    name='Base Marker'
))

# Orientation arrows
arrows = {axis:{'x':[], 'y':[], 'z':[]} for axis in ['X','Y','Z']}
span = np.max(np.ptp(rel_rot, axis=1))
L = arrow_scale * span
for i in range(0, unit_vs.shape[1], sample_step):
    x0, y0, z0 = rot[:, i]
    ux, uy, uz = unit_vs[:, i]
    a = arrows['X']
    a['x'] += [x0, x0+L*ux, None]
    a['y'] += [y0, y0+L*uy, None]
    a['z'] += [z0, z0+L*uz, None]
    a = arrows['Y']
    a['x'] += [x0, x0-L*uy, None]
    a['y'] += [y0, y0+L*ux, None]
    a['z'] += [z0, z0,       None]
    a = arrows['Z']
    a['x'] += [x0, x0,       None]
    a['y'] += [y0, y0,       None]
    a['z'] += [z0, z0+L,   None]
for axis, col in zip(['X','Y','Z'], [color_arrow_x, color_arrow_y, color_arrow_z]):
    arr = arrows[axis]
    fig.add_trace(go.Scatter3d(
        x=arr['x'], y=arr['y'], z=arr['z'], mode='lines',
        line=dict(color=col, width=arrow_width), name=f'{axis}-axis'
    ))

# Layout with custom legend & axis fonts
fig.update_layout(
    legend=dict(font=dict(family=legend_font_family, size=legend_font_size)),
    scene=dict(
        xaxis=dict(
            title='<b>X (mm)</b>', titlefont=dict(family=axis_title_font_family, size=axis_title_font_size),
            tickfont=dict(family=axis_title_font_family, size=axis_tick_font_size),
            gridcolor=scene_axis_line_color, backgroundcolor=scene_bgcolor
        ),
        yaxis=dict(
            title='<b>Y (mm)</b>', titlefont=dict(family=axis_title_font_family, size=axis_title_font_size),
            tickfont=dict(family=axis_title_font_family, size=axis_tick_font_size),
            gridcolor=scene_axis_line_color, backgroundcolor=scene_bgcolor
        ),
        zaxis=dict(
            title='<b>Z (mm)</b>', titlefont=dict(family=axis_title_font_family, size=axis_title_font_size),
            tickfont=dict(family=axis_title_font_family, size=axis_tick_font_size),
            gridcolor=scene_axis_line_color, backgroundcolor=scene_bgcolor
        ),
        aspectmode='auto'
    ),
    width=window_width, height=window_height
)

fig.show()