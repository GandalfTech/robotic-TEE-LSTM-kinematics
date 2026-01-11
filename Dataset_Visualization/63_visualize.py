import scipy.io
import numpy as np
import plotly.graph_objects as go
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

rx, ry, rz = 0, -20, 40
line_width = 8
color = 'rgb(214, 39, 40)'  # Red
base_marker_color = 'limegreen'

data = scipy.io.loadmat("Robot_Data_90F.mat")

def rotation_matrix(rx, ry, rz):
    rx, ry, rz = np.radians([rx, ry, rz])
    Rx = np.array([[1, 0, 0], [0, np.cos(rx), -np.sin(rx)], [0, np.sin(rx), np.cos(rx)]])
    Ry = np.array([[np.cos(ry), 0, np.sin(ry)], [0, 1, 0], [-np.sin(ry), 0, np.cos(ry)]])
    Rz = np.array([[np.cos(rz), -np.sin(rz), 0], [np.sin(rz), np.cos(rz), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

def process_and_rotate(data, R):
    ir1 = data['ir_positions']
    ir2 = data['ir_positions2']
    rel = ir1 - ir2
    rel_mm = np.vstack([rel[0], rel[2], -rel[1]]) * 1000
    return R @ rel_mm

R = rotation_matrix(rx, ry, rz)
X, Y, Z = process_and_rotate(data, R)

fig = go.Figure()
fig.add_trace(go.Scatter3d(x=X, y=Y, z=Z, mode='lines',
    line=dict(color=color, width=line_width), name='90° Bending'))
fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers',
    marker=dict(size=10, color=base_marker_color, symbol='diamond'), name='Base Marker'))

fig.update_layout(
    title=f"<b>90° Bending Trajectory</b>",
    scene=dict(
        xaxis=dict(title='X (mm)', gridcolor='lightgray', backgroundcolor='#f4f4f4'),
        yaxis=dict(title='Y (mm)', gridcolor='lightgray', backgroundcolor='#f4f4f4'),
        zaxis=dict(title='Z (mm)', gridcolor='lightgray', backgroundcolor='#f4f4f4'),
        bgcolor='#f4f4f4'
    ),
    width=900, height=750
)

fig.show()
