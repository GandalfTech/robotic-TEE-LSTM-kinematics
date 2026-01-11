import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.lines import Line2D

# ========= USER CONFIGURATION =========

mat_files = {
    'Zero': 'Robot_Data_Zero.mat',
    '45': 'Robot_Data3_45.mat',
    '90': 'Robot_Data_90F.mat'
}

rotation_angles = (0, -20, 40)
output_dir = 'output_results'
os.makedirs(output_dir, exist_ok=True)

# Title and axis labels
plot_title = "Boxplot of Positional Deviations"
x_label = "Dataset"
y_label_template = "{}-axis (mm)"

# X-axis tick labels (multi-line format) for X only
x_tick_labels = [
    "X Original\nZero Dataset", "X Rotated\nZero Dataset",
    "X Original\n45° Dataset", "X Rotated\n45° Dataset",
    "X Original\n90° Dataset", "X Rotated\n90° Dataset"
]

# Colors
color_map = {
    ('Zero', 'Before Rotation'): '#1a5276',
    ('Zero', 'After Rotation'): '#7fb3d5',
    ('45', 'Before Rotation'): '#283747',
    ('45', 'After Rotation'): '#85929e',
    ('90', 'Before Rotation'): '#512e5f',
    ('90', 'After Rotation'): '#9b59b6',
}

# color_map = {
#     ('Zero', 'Before Rotation'): '#1b2631',
#     ('Zero', 'After Rotation'): '#515a5a',
#     ('45', 'Before Rotation'): '#2980b9',
#     ('45', 'After Rotation'): '#3498db',
#     ('90', 'Before Rotation'): '#922b21',
#     ('90', 'After Rotation'): '#cb4335',
# }

image_dpi = 300

# ========= FUNCTIONS ==========

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
    return rel_pos_mm, rotated

# ========= DATA PROCESSING =========

R = rotation_matrix(*rotation_angles)
stats = []
box_data = []

for label, file_path in mat_files.items():
    data = scipy.io.loadmat(file_path)
    raw, rotated = process_and_rotate(data, R)
    for axis_idx, axis_label in enumerate(['X', 'Y', 'Z']):
        stats.extend([
            {
                'Dataset': label, 'Axis': axis_label, 'Stage': 'Before Rotation',
                'Mean': np.mean(raw[axis_idx]), 'Std': np.std(raw[axis_idx]),
                'Min': np.min(raw[axis_idx]), 'Max': np.max(raw[axis_idx])
            },
            {
                'Dataset': label, 'Axis': axis_label, 'Stage': 'After Rotation',
                'Mean': np.mean(rotated[axis_idx]), 'Std': np.std(rotated[axis_idx]),
                'Min': np.min(rotated[axis_idx]), 'Max': np.max(rotated[axis_idx])
            }
        ])
        for val in raw[axis_idx]:
            box_data.append({'Dataset': label, 'Axis': axis_label, 'Stage': 'Before Rotation', 'Value': val})
        for val in rotated[axis_idx]:
            box_data.append({'Dataset': label, 'Axis': axis_label, 'Stage': 'After Rotation', 'Value': val})

# Save data
pd.DataFrame(box_data).to_csv(os.path.join(output_dir, 'axis_data_before_after_rotation.csv'), index=False)
pd.DataFrame(stats).to_csv(os.path.join(output_dir, 'descriptive_stats.csv'), index=False)

# ========= BOXPLOTS FORMATTED =========

for axis in ['X', 'Y', 'Z']:
    plt.figure(figsize=(12, 6))
    current_pos = 0
    box_positions = []

    for dataset in ['Zero', '45', '90']:
        for stage in ['Before Rotation', 'After Rotation']:
            subset = pd.DataFrame(box_data)[
                (pd.DataFrame(box_data)['Axis'] == axis) &
                (pd.DataFrame(box_data)['Dataset'] == dataset) &
                (pd.DataFrame(box_data)['Stage'] == stage)
            ]
            color = color_map[(dataset, stage)]

            plt.boxplot(
                subset['Value'],
                positions=[current_pos],
                widths=0.6,
                patch_artist=True,
                boxprops=dict(
                    facecolor=color + '80',  # Add alpha (~50% transparency) using hex
                    edgecolor='black',       # Solid black border
                    linewidth=1.5
                ),
                medianprops=dict(color='black', linewidth=2),  # Adjust to match your red style
                whiskerprops=dict(color='black', linewidth=2, linestyle='--'),
                capprops=dict(color='black', linewidth=2),
                flierprops=dict(marker='o', markerfacecolor='black', markersize=2, linestyle='none'),
                meanprops=dict(marker='o', markerfacecolor='#d7dbdd', markeredgecolor='black', markersize=8),
                showmeans=True,
                showfliers=False
            )


            ###########REZA
            # plt.boxplot(
            #     subset['Value'],
            #     positions=[current_pos],
            #     widths=0.6,
            #     patch_artist=True,
            #     boxprops=dict(facecolor=color, edgecolor=color, linewidth=2),
            #     medianprops=dict(color='#bdc3c7', linewidth=2),
            #     whiskerprops=dict(color='black', linewidth=2, linestyle='--'),
            #     capprops=dict(color=color, linewidth=2),
            #     flierprops=dict(marker='o', markerfacecolor='black', markersize=0, linestyle='none'),
            #     meanprops=dict(marker='o', markerfacecolor='green', markeredgecolor='purple', markersize=8),
            #     showmeans=True
            # )
            box_positions.append(current_pos)
            current_pos += 1

    if axis == 'X':
        plt.xticks(box_positions, x_tick_labels, fontsize=10)
    else:
        default_labels = [
            f"{axis} Original\nZero Dataset", f"{axis} Rotated\nZero Dataset",
            f"{axis} Original\n45° Dataset", f"{axis} Rotated\n45° Dataset",
            f"{axis} Original\n90° Dataset", f"{axis} Rotated\n90° Dataset"
        ]
        plt.xticks(box_positions, default_labels, fontsize=10)

    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label_template.format(axis), fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.4)

    # Legend
    legend_elements = [
        Line2D([0], [0], color='black', lw=2, label='Median'),
        Line2D([0], [0], marker='o', color='black', markerfacecolor='#d7dbdd',
               markersize=8, linestyle='None', label='Mean'),
        Line2D([0], [0], color='black', lw=2, linestyle='--', label='Whiskers')
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=10, frameon=False)

    plt.tight_layout()
    output_path = os.path.join(output_dir, f'{axis}_axis_boxplot.png')
    plt.savefig(output_path, dpi=image_dpi, bbox_inches='tight')
    print(f"📊 Saved: {output_path}")
    plt.close()

print("✔ All plots saved.")
