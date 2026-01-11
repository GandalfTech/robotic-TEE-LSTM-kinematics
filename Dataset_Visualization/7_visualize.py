import scipy.io
import numpy as np
import plotly.graph_objects as go
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

# === USER SETTINGS ===
rx, ry, rz = 0, -20, 40
line_width_0 = 8
line_width_45 = 8
line_width_90 = 8
gastroscope_diameter = 16  # mm
gastroscope_radius = gastroscope_diameter / 2

# Colors
color_0 = 'rgb(0, 0, 255)'  # Blue
color_45 = 'black'
color_90 = 'rgb(214, 39, 40)'  # Red
base_marker_color = 'limegreen'
tube_color = 'rgba(100,100,100,0.5)'

# Rotation and transformation
def rotation_matrix(rx, ry, rz):
    rx, ry, rz = np.radians([rx, ry, rz])
    Rx = np.array([[1, 0, 0], [0, np.cos(rx), -np.sin(rx)], [0, np.sin(rx), np.cos(rx)]])
    Ry = np.array([[np.cos(ry), 0, np.sin(ry)], [0, 1, 0], [-np.sin(ry), 0, np.cos(ry)]])
    Rz = np.array([[np.cos(rz), -np.sin(rz), 0], [np.sin(rz), np.cos(rz), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

def process_and_rotate(data, R):
    ir_positions = data['ir_positions']
    ir_positions2 = data['ir_positions2']
    rel_pos = ir_positions - ir_positions2
    rel_pos_mm = np.vstack([rel_pos[0], rel_pos[2], -rel_pos[1]]) * 1000
    rotated = R @ rel_pos_mm
    return rotated[0], rotated[1], rotated[2]

# Load and transform
data_zero = scipy.io.loadmat("Robot_Data_Zero.mat")
data_45 = scipy.io.loadmat("Robot_Data3_45.mat")
data_90 = scipy.io.loadmat("Robot_Data_90F.mat")
R = rotation_matrix(rx, ry, rz)
X0, Y0, Z0 = process_and_rotate(data_zero, R)
X45, Y45, Z45 = process_and_rotate(data_45, R)
X90, Y90, Z90 = process_and_rotate(data_90, R)

# Gastroscope tube as a cylinder from origin to midpoint
def add_gastroscope(fig, X, Y, Z, color, label):
    mid_idx = len(X) // 2
    xm, ym, zm = X[mid_idx], Y[mid_idx], Z[mid_idx]

    fig.add_trace(go.Scatter3d(
        x=[0, xm], y=[0, ym], z=[0, zm],
        mode='lines',
        line=dict(color=color, width=gastroscope_diameter),
        name=f'{label} Gastroscope Tube'
    ))

# Create figure
fig = go.Figure()

# Plot gastroscope tubes (origin to midpoint)
add_gastroscope(fig, X0, Y0, Z0, color_0, '0°')
add_gastroscope(fig, X45, Y45, Z45, color_45, '45°')
add_gastroscope(fig, X90, Y90, Z90, color_90, '90°')

# Plot bending trajectories
def add_trajectory(fig, x, y, z, color, label, width):
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color=color, width=width),
        name=f'{label} Bending'
    ))

add_trajectory(fig, X0, Y0, Z0, color_0, "0°", line_width_0)
add_trajectory(fig, X45, Y45, Z45, color_45, "45°", line_width_45)
add_trajectory(fig, X90, Y90, Z90, color_90, "90°", line_width_90)

# Base Marker
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=10, color=base_marker_color, symbol='diamond'),
    name='Base Marker'
))

# Layout
fig.update_layout(
    title=dict(
        text=f"<b>TEE Probe: Gastroscope Tube + Bending Section</b><br><span style='font-size:12px'>Rotated X={rx}°, Y={ry}°, Z={rz}°, Tube Ø={gastroscope_diameter}mm</span>",
        font=dict(size=22), x=0.5
    ),
    scene=dict(
        xaxis=dict(title='X (mm)', showgrid=True),
        yaxis=dict(title='Y (mm)', showgrid=True),
        zaxis=dict(title='Z (mm)', showgrid=True),
        bgcolor='white',
        aspectmode='data'
    ),
    legend=dict(font=dict(size=14), bordercolor='lightgray', borderwidth=1),
    margin=dict(l=10, r=10, b=10, t=50),
    width=1000,
    height=800
)

fig.show()
