import scipy.io
import numpy as np
import plotly.graph_objects as go
from scipy.spatial.transform import Rotation as R
import warnings

# Suppress .mat file loading warnings
warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

# === USER SETTINGS ===
rx, ry, rz = 0, 0, 0            # global rotation angles (degrees)
window_width, window_height = 1800, 1100
start_index, end_index = 0, None
line_width   = 6
arrow_scale  = 0.06
arrow_width  = 2
sample_step  = 10                  # draw every Nth quaternion

# Base‐marker styling
base_marker_size   = 30
base_marker_color  = 'black'
base_marker_symbol = 'circle'

# Fonts & scene styling
legend_font_family     = 'Arial'
legend_font_size       = 14
axis_title_font_family = 'Arial'
axis_title_font_size   = 16
axis_title_bold        = True
axis_tick_font_size    = 12
scene_bgcolor          = 'white'
scene_axis_line_color  = 'gray'

# Colors
traj_color    = 'black'   # single color for all trajectories
color_arrow_x = 'red'     # body‐frame X
color_arrow_y = 'green'   # body‐frame Y
color_arrow_z = 'blue'    # body‐frame Z

datasets = [
    {'file':'Robot_Data_Zero.mat',  'label':'Zero'},
    {'file':'Robot_Data_90F.mat',   'label':'90° Forward'},
    {'file':'Robot_Data3_45.mat',   'label':'45°'},
]

def rotation_matrix(rx, ry, rz):
    rx, ry, rz = np.radians([rx, ry, rz])
    Rx = np.array([[1,0,0],
                   [0,np.cos(rx),-np.sin(rx)],
                   [0,np.sin(rx), np.cos(rx)]])
    Ry = np.array([[ np.cos(ry),0,np.sin(ry)],
                   [0,1,0],
                   [-np.sin(ry),0,np.cos(ry)]])
    Rz = np.array([[ np.cos(rz),-np.sin(rz),0],
                   [ np.sin(rz), np.cos(rz),0],
                   [0,0,1]])
    return Rz @ Ry @ Rx

Rmat = rotation_matrix(rx, ry, rz)
fig = go.Figure()

# control legend display
draw_traj_legend = True
draw_axes_legend = True

for ds in datasets:
    data   = scipy.io.loadmat(ds['file'], squeeze_me=True)
    ir1, ir2 = data['ir_positions'], data['ir_positions2']
    qw, qv   = data['ir_quaternion_scalar'], data['ir_quaternion_vector']

    # --- rotated trajectory ---
    rel_mm  = np.vstack([ir1[0]-ir2[0],
                         ir1[2]-ir2[2],
                         -(ir1[1]-ir2[1])]) * 1000
    rel_rot = Rmat @ rel_mm
    x, y, z = rel_rot[:, start_index:end_index]

    # only show this legend entry once
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color=traj_color, width=line_width),
        name='Original Trajectories',
        legendgroup='pos',
        showlegend=draw_traj_legend
    ))
    draw_traj_legend = False

    # --- build & rotate quaternions into body‐frame axes ---
    quats  = np.vstack([qv, qw]).T
    Rs     = R.from_quat(quats).as_matrix()
    Rs_tot = np.einsum('ij,kjl->kil', Rmat, Rs)

    # --- sample & collect arrows ---
    arrows = {ax:{'x':[], 'y':[], 'z':[]} for ax in ('X','Y','Z')}
    span   = np.max(np.ptp(rel_rot, axis=1))
    L      = arrow_scale * span
    n_end  = rel_rot.shape[1] if end_index is None else end_index

    for i in range(start_index, n_end, sample_step):
        x0, y0, z0 = rel_rot[:, i]
        R_i        = Rs_tot[i]

        # Body‐frame X‐axis
        ux, uy, uz = R_i[:,0]
        a = arrows['X']
        a['x'] += [x0, x0 + L*ux, None]
        a['y'] += [y0, y0 + L*uy, None]
        a['z'] += [z0, z0 + L*uz, None]

        # Body‐frame Y‐axis
        vx, vy, vz = R_i[:,1]
        a = arrows['Y']
        a['x'] += [x0, x0 + L*vx, None]
        a['y'] += [y0, y0 + L*vy, None]
        a['z'] += [z0, z0 + L*vz, None]

        # Body‐frame Z‐axis
        wx, wy, wz = R_i[:,2]
        a = arrows['Z']
        a['x'] += [x0, x0 + L*wx, None]
        a['y'] += [y0, y0 + L*wy, None]
        a['z'] += [z0, z0 + L*wz, None]

    # only show these three axes legend entries once
    legend_opts = dict(legendgroup='body_frame_axes', showlegend=draw_axes_legend)
    draw_axes_legend = False

    fig.add_trace(go.Scatter3d(
        x=arrows['X']['x'], y=arrows['X']['y'], z=arrows['X']['z'],
        mode='lines', line=dict(color=color_arrow_x, width=arrow_width),
        name='X-axis',
        **legend_opts
    ))
    fig.add_trace(go.Scatter3d(
        x=arrows['Y']['x'], y=arrows['Y']['y'], z=arrows['Y']['z'],
        mode='lines', line=dict(color=color_arrow_y, width=arrow_width),
        name='Y-axis',
        **legend_opts
    ))
    fig.add_trace(go.Scatter3d(
        x=arrows['Z']['x'], y=arrows['Z']['y'], z=arrows['Z']['z'],
        mode='lines', line=dict(color=color_arrow_z, width=arrow_width),
        name='Z-axis',
        **legend_opts
    ))

# base marker
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=base_marker_size, color=base_marker_color, symbol=base_marker_symbol),
    name='Base Marker'
))

# === layout & legend positioning ===
def font_dict(fam, sz, bold=False):
    d = dict(family=fam, size=sz, color='black')
    if bold: d['family'] += ', bold'
    return d

fig.update_layout(
    legend=dict(
        font=dict(family=legend_font_family, size=legend_font_size),
        # Position anywhere you like by adjusting x/y and anchors:
        x=0.7,            # 0=left margin, 1=right margin
        y=0.8,            # 0=bottom, 1=top
        xanchor='right',   # anchor the legend's right side at x
        yanchor='top',     # anchor the legend's top at y
        orientation='v'    # 'v' = vertical, 'h' = horizontal
    ),
    scene=dict(
        xaxis=dict(
            title='<b>X (mm)</b>',
            titlefont=font_dict(axis_title_font_family, axis_title_font_size, axis_title_bold),
            tickfont=font_dict(axis_title_font_family, axis_tick_font_size),
            gridcolor=scene_axis_line_color,
            backgroundcolor=scene_bgcolor
        ),
        yaxis=dict(
            title='<b>Y (mm)</b>',
            titlefont=font_dict(axis_title_font_family, axis_title_font_size, axis_title_bold),
            tickfont=font_dict(axis_title_font_family, axis_tick_font_size),
            gridcolor=scene_axis_line_color,
            backgroundcolor=scene_bgcolor
        ),
        zaxis=dict(
            title='<b>Z (mm)</b>',
            titlefont=font_dict(axis_title_font_family, axis_title_font_size, axis_title_bold),
            tickfont=font_dict(axis_title_font_family, axis_tick_font_size),
            gridcolor=scene_axis_line_color,
            backgroundcolor=scene_bgcolor
        ),
        aspectmode='auto'
    ),
    width=window_width,
    height=window_height
)

fig.show()
