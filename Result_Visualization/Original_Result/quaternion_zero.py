import scipy.io
import numpy as np
import plotly.graph_objects as go
import warnings

# Suppress .mat file loading warnings
warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

# === USER SETTINGS ===
rx, ry, rz = 0, 0, 0          # global rotation (degrees)
window_width, window_height = 1800, 1100

#start_index, end_index = 2000, 9000
start_index, end_index = 9780, None
sample_step = 50                  # draw orientation arrows every N samples
line_width = 6
arrow_scale = 0.15
arrow_width = 2

# Marker origin styling
base_marker_size = 30
base_marker_color = 'black'
base_marker_symbol = 'circle'

# Font settings
legend_font_family = 'Arial'
legend_font_size = 14
axis_title_font_family = 'Arial'
axis_title_font_size = 16
axis_tick_font_size = 12

# Scene styling
scene_bgcolor = 'white'
scene_axis_line_color = 'gray'

# Colors — measured vs predicted
color_meas = "#043e63"
color_pred = "#ec0960"

# Arrow colors (Measured)
color_meas_arrow_x = "#f11847"
color_meas_arrow_y = "#022061"
color_meas_arrow_z = "#045f0c"
# Arrow colors (Predicted)
color_pred_arrow_x = "#df5634"
color_pred_arrow_y = "#1A48DF"
color_pred_arrow_z = "#1eac19"


# --- Helpers ---
def rotation_matrix(rx, ry, rz):
    rx, ry, rz = np.radians([rx, ry, rz])
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rx), -np.sin(rx)],
                   [0, np.sin(rx),  np.cos(rx)]])
    Ry = np.array([[ np.cos(ry), 0, np.sin(ry)],
                   [ 0,          1, 0        ],
                   [-np.sin(ry), 0, np.cos(ry)]])
    Rz = np.array([[ np.cos(rz), -np.sin(rz), 0],
                   [ np.sin(rz),  np.cos(rz), 0],
                   [ 0,            0,          1]])
    return Rz @ Ry @ Rx


def add_arrows(fig, x, y, z, ox, oy, oz,
               color_x, color_y, color_z, prefix_label):
    """Add X, Y, Z orientation arrows, legend once, with custom axis-pair labels."""
    span = np.max([np.ptp(x), np.ptp(y), np.ptp(z)])
    L = arrow_scale * span
    N = len(x)
    for idx in range(0, N, sample_step):
        bx, by, bz = x[idx], y[idx], z[idx]
        ux, uy, uz = ox[idx], oy[idx], oz[idx]
        norm = np.linalg.norm([ux, uy, uz])
        if norm == 0:
            continue
        ux, uy, uz = ux / norm, uy / norm, uz / norm

        show_first = (idx == 0)

        # X‐axis arrow
        fig.add_trace(go.Scatter3d(
            x=[bx, bx + L * ux],
            y=[by, by + L * uy],
            z=[bz, bz + L * uz],
            mode='lines',
            line=dict(color=color_x, width=arrow_width),
            name=f'X-axis-{prefix_label}',
            showlegend=show_first
        ))

        # Y‐axis arrow (perp in XY)
        fig.add_trace(go.Scatter3d(
            x=[bx, bx + L * uy],
            y=[by, by - L * ux],
            z=[bz, bz],
            mode='lines',
            line=dict(color=color_y, width=arrow_width),
            name=f'Y-axis-{prefix_label}',
            showlegend=show_first
        ))

        # Z‐axis arrow (vertical)
        fig.add_trace(go.Scatter3d(
            x=[bx, bx],
            y=[by, by],
            z=[bz, bz + L],
            mode='lines',
            line=dict(color=color_z, width=arrow_width),
            name=f'Z-axis-{prefix_label}',
            showlegend=show_first
        ))


def load_and_slice(matfile, key):
    """Load a .mat variable and slice it by start/end indices."""
    arr = scipy.io.loadmat(matfile)[key].squeeze()
    return arr[start_index:end_index]


# === LOAD AND SLICE DATA ===
# Positions (mm)
x0  = load_and_slice("TEE_Zero_org_pos_matlab.mat",     'x_total') * 1000
y0  = load_and_slice("TEE_Zero_org_pos_matlab.mat",     'y_total') * 1000
z0  = load_and_slice("TEE_Zero_org_pos_matlab.mat",     'z_total') * 1000
xp0 = load_and_slice("TEE_Zero_predict_pos_matlab.mat", 'xp_total') * 1000
yp0 = load_and_slice("TEE_Zero_predict_pos_matlab.mat", 'yp_total') * 1000
zp0 = load_and_slice("TEE_Zero_predict_pos_matlab.mat", 'zp_total') * 1000

# Orientations
ox0  = load_and_slice("TEE_Zero_org_orient_matlab.mat",     'o1_total')
oy0  = load_and_slice("TEE_Zero_org_orient_matlab.mat",     'o2_total')
oz0  = load_and_slice("TEE_Zero_org_orient_matlab.mat",     'o3_total')
oxp0 = load_and_slice("TEE_Zero_predict_orient_matlab.mat", 'o1p_total')
oyp0 = load_and_slice("TEE_Zero_predict_orient_matlab.mat", 'o2p_total')
ozp0 = load_and_slice("TEE_Zero_predict_orient_matlab.mat", 'o3p_total')

# === APPLY GLOBAL ROTATION ===
Rmat = rotation_matrix(rx, ry, rz)

meas = Rmat @ np.vstack([x0, y0, z0])
pred = Rmat @ np.vstack([xp0, yp0, zp0])
oxr  = Rmat @ np.vstack([ox0, oy0, oz0])
oxpr = Rmat @ np.vstack([oxp0, oyp0, ozp0])

# Unpack
mx, my, mz             = meas
px, py, pz             = pred
oxr_x, oxr_y, ozr_z     = oxr
oxpr_x, oxpr_y, ozpr_z = oxpr


# === BUILD FIGURE ===
fig = go.Figure()

# Trajectories
fig.add_trace(go.Scatter3d(
    x=mx, y=my, z=mz,
    mode='lines',
    line=dict(color=color_meas, width=line_width),
    name='Measured Trajectory'
))
fig.add_trace(go.Scatter3d(
    x=px, y=py, z=pz,
    mode='lines',
    line=dict(color=color_pred, width=line_width),
    name='Predicted Trajectory'
))

# # Marker Origin
# fig.add_trace(go.Scatter3d(
#     x=[0], y=[0], z=[0],
#     mode='markers',
#     marker=dict(size=base_marker_size, color=base_marker_color, symbol=base_marker_symbol),
#     name='Origin'
# ))

# Orientation arrows with updated labels
add_arrows(
    fig,
    mx, my, mz,
    oxr_x, oxr_y, ozr_z,
    color_meas_arrow_x, color_meas_arrow_y, color_meas_arrow_z,
    prefix_label='Original'
)
add_arrows(
    fig,
    px, py, pz,
    oxpr_x, oxpr_y, ozpr_z,
    color_pred_arrow_x, color_pred_arrow_y, color_pred_arrow_z,
    prefix_label='Prediction'
)

# === LAYOUT ===
fig.update_layout(
    legend=dict(font=dict(family=legend_font_family, size=legend_font_size)),
    scene=dict(
        xaxis=dict(
            title="<b>X (mm)</b>",
            titlefont=dict(family=axis_title_font_family, size=axis_title_font_size),
            tickfont=dict(size=axis_tick_font_size),
            gridcolor=scene_axis_line_color,
            backgroundcolor=scene_bgcolor
        ),
        yaxis=dict(
            title="<b>Y (mm)</b>",
            titlefont=dict(family=axis_title_font_family, size=axis_title_font_size),
            tickfont=dict(size=axis_tick_font_size),
            gridcolor=scene_axis_line_color,
            backgroundcolor=scene_bgcolor
        ),
        zaxis=dict(
            title="<b>Z (mm)</b>",
            titlefont=dict(family=axis_title_font_family, size=axis_title_font_size),
            tickfont=dict(size=axis_tick_font_size),
            gridcolor=scene_axis_line_color,
            backgroundcolor=scene_bgcolor
        ),
        aspectmode='auto'
    ),
    width=window_width,
    height=window_height
)

fig.show()
