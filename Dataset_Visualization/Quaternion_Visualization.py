import scipy.io
import numpy as np
import plotly.graph_objects as go
import warnings

# Suppress .mat file loading warnings
warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

# === USER SETTINGS ===
rx, ry, rz = 0, -20, 40          # global rotation (degrees)
window_width, window_height = 1600, 1000
start_index, end_index = 0, None
sample_step = 50                  # draw orientation arrows every N samples
line_width = 6
arrow_scale = 0.15                # ← doubled from 0.05 for bigger axes
arrow_width = 2

# Marker origin styling
base_marker_size = 16             # ↑ you can increase this for a bigger dot
base_marker_color = 'black'
base_marker_symbol = 'circle'

scene_bgcolor = 'white'
scene_axis_line_color = 'gray'
axis_tick_font_size = 12
axis_font_family = 'Arial'

# Colors
color_original = '#5499c7'
color_traj     = '#154360'
color_arrow_x  = 'red'
color_arrow_y  = 'green'
color_arrow_z  = 'blue'

# === Helper: Rotation matrix ===
def rotation_matrix(rx, ry, rz):
    rx, ry, rz = np.radians([rx, ry, rz])
    Rx = np.array([[1,0,0],
                   [0,np.cos(rx),-np.sin(rx)],
                   [0,np.sin(rx), np.cos(rx)]])
    Ry = np.array([[ np.cos(ry), 0, np.sin(ry)],
                   [ 0,         1, 0        ],
                   [-np.sin(ry),0, np.cos(ry)]])
    Rz = np.array([[ np.cos(rz), -np.sin(rz), 0],
                   [ np.sin(rz),  np.cos(rz), 0],
                   [ 0,           0,          1]])
    return Rz @ Ry @ Rx

# === Load data ===
data = scipy.io.loadmat("Robot_Data_Zero.mat")
ir1 = data['ir_positions']
ir2 = data['ir_positions2']

# Compute relative position (tool w.r.t. marker origin)
rel = ir1 - ir2            # 3×N
rel_mm = np.vstack([rel[0], rel[2], -rel[1]]) * 1000  # reorder & mm

# Apply global rotation
R = rotation_matrix(rx, ry, rz)
rel_rot = R @ rel_mm

# Slice for plotting
orig_x, orig_y, orig_z = rel_mm[:, start_index:end_index]
X, Y, Z               = rel_rot[:, start_index:end_index]

# Orientation unit vectors
vecs    = rel_rot[:, start_index:end_index]
norms   = np.linalg.norm(vecs, axis=0)
unit_vs = vecs / norms

# Build figure
fig = go.Figure()

# Original trajectory
fig.add_trace(go.Scatter3d(
    x=orig_x, y=orig_y, z=orig_z,
    mode='lines', line=dict(color=color_original, width=line_width),
    name='Original Trajectory'
))

# Rotated trajectory
fig.add_trace(go.Scatter3d(
    x=X, y=Y, z=Z,
    mode='lines', line=dict(color=color_traj, width=line_width),
    name='Rotated Trajectory'
))

# Marker origin at (0,0,0)
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=base_marker_size, color=base_marker_color, symbol=base_marker_symbol),
    name='Marker Origin'
))

# Orientation arrows
arrows = {axis:{'x':[], 'y':[], 'z':[]} for axis in ['X','Y','Z']}
span   = np.max(np.ptp(rel_rot, axis=1))
L      = arrow_scale * span

for i in range(0, unit_vs.shape[1], sample_step):
    x0, y0, z0 = rel_rot[:, i]
    ux, uy, uz = unit_vs[:, i]

    # X-axis arrow (along orientation)
    a = arrows['X']
    a['x'] += [x0, x0 + L*ux, None]
    a['y'] += [y0, y0 + L*uy, None]
    a['z'] += [z0, z0 + L*uz, None]

    # Y-axis arrow (perp in XY plane)
    a = arrows['Y']
    a['x'] += [x0, x0 - L*uy, None]
    a['y'] += [y0, y0 + L*ux, None]
    a['z'] += [z0, z0,       None]

    # Z-axis arrow (vertical)
    a = arrows['Z']
    a['x'] += [x0, x0,       None]
    a['y'] += [y0, y0,       None]
    a['z'] += [z0, z0 + L,   None]

# Add arrow traces
for axis, col in zip(['X','Y','Z'], [color_arrow_x, color_arrow_y, color_arrow_z]):
    arr = arrows[axis]
    fig.add_trace(go.Scatter3d(
        x=arr['x'], y=arr['y'], z=arr['z'],
        mode='lines',
        line=dict(color=col, width=arrow_width),
        name=f'{axis}-axis'
    ))

# Layout
fig.update_layout(
    title='Tool Trajectory Relative to Marker Position',
    scene=dict(
        xaxis=dict(title='X (mm)', gridcolor=scene_axis_line_color, backgroundcolor=scene_bgcolor),
        yaxis=dict(title='Y (mm)', gridcolor=scene_axis_line_color, backgroundcolor=scene_bgcolor),
        zaxis=dict(title='Z (mm)', gridcolor=scene_axis_line_color, backgroundcolor=scene_bgcolor),
        aspectmode='auto'
    ),
    width=window_width, height=window_height
)
fig.show()
