import scipy.io
import numpy as np
import plotly.graph_objects as go
import warnings

# Suppress .mat file loading warnings
warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

# === USER SETTINGS: Rotation Angles ===
rx, ry, rz = 0, -20, -40  # degrees

# === USER SETTINGS: Line Width ===
line_width_0 = 8
line_width_45 = 8
line_width_90 = 8

# === USER SETTINGS: Colors ===
color_0 = 'rgb(0, 0, 255)'        # Blue
color_45 = 'black'                # Black
color_90 = 'rgb(214, 39, 40)'     # Red
base_marker_color = 'limegreen'

# === Data Loading ===
data_zero = scipy.io.loadmat("Robot_Data_Zero.mat")
data_45 = scipy.io.loadmat("Robot_Data3_45.mat")
data_90 = scipy.io.loadmat("Robot_Data_90F.mat")

# === Rotation matrix helper ===
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

# === Process and rotate data ===
def process_and_rotate(data, R):
    ir_positions = data['ir_positions']
    ir_positions2 = data['ir_positions2']
    rel_pos = ir_positions - ir_positions2
    rel_pos_mm = np.vstack([rel_pos[0], rel_pos[2], -rel_pos[1]]) * 1000
    rotated = R @ rel_pos_mm
    return rotated[0], rotated[1], rotated[2]

# === Compute transformations ===
R = rotation_matrix(rx, ry, rz)
X0, Y0, Z0 = process_and_rotate(data_zero, R)
X45, Y45, Z45 = process_and_rotate(data_45, R)
X90, Y90, Z90 = process_and_rotate(data_90, R)

# === Create 3D interactive plot ===
fig = go.Figure()

# 0° Bending
fig.add_trace(go.Scatter3d(
    x=X0, y=Y0, z=Z0,
    mode='lines',
    line=dict(color=color_0, width=line_width_0),
    name='0° Bending'
))

# 45° Bending
fig.add_trace(go.Scatter3d(
    x=X45, y=Y45, z=Z45,
    mode='lines',
    line=dict(color=color_45, width=line_width_45),
    name='45° Bending'
))

# 90° Bending
fig.add_trace(go.Scatter3d(
    x=X90, y=Y90, z=Z90,
    mode='lines',
    line=dict(color=color_90, width=line_width_90),
    name='90° Bending'
))

# Base Marker
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=10, color=base_marker_color, symbol='diamond'),
    name='Base Marker'
))

# === Layout with better background ===
fig.update_layout(
    title=dict(
        text=f"<b>3D Gastroscope Bending Trajectories</b><br><span style='font-size:12px'>Rotated X={rx}°, Y={ry}°, Z={rz}°</span>",
        font=dict(size=22),
        x=0.5
    ),
    scene=dict(
        xaxis=dict(title=dict(text='X (mm)', font=dict(size=16)),
                   tickfont=dict(size=12),
                   gridcolor='lightgray',
                   zerolinecolor='gray',
                   showbackground=True,
                   backgroundcolor='#f4f4f4'),
        yaxis=dict(title=dict(text='Y (mm)', font=dict(size=16)),
                   tickfont=dict(size=12),
                   gridcolor='lightgray',
                   zerolinecolor='gray',
                   showbackground=True,
                   backgroundcolor='#f4f4f4'),
        zaxis=dict(title=dict(text='Z (mm)', font=dict(size=16)),
                   tickfont=dict(size=12),
                   gridcolor='lightgray',
                   zerolinecolor='gray',
                   showbackground=True,
                   backgroundcolor='white'),
        bgcolor='white'
    ),
    legend=dict(font=dict(size=14), bordercolor='lightgray', borderwidth=1),
    margin=dict(l=10, r=10, b=10, t=50),
    width=1000,
    height=800
)

fig.show()
