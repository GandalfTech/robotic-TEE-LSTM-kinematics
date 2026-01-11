import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ========= CONFIGURATION =========

# Input MATLAB files
mat_files = {
    'Zero': 'Robot_Data_Zero.mat',
    '45': 'Robot_Data3_45.mat',
    '90': 'Robot_Data_90F.mat'
}

# Rotation angles (in degrees)
rx, ry, rz = 0, -20, 40

# Output directory
output_dir = 'output_results'
os.makedirs(output_dir, exist_ok=True)

# Custom color scheme
color_map = {
    ('Zero', 'Before Rotation'): '#1a5276',   # deep blue
    ('Zero', 'After Rotation'):  '#7fb3d5',   # light blue
    ('45',   'Before Rotation'): '#283747',   # dark gray/blue
    ('45',   'After Rotation'):  '#85929e',   # light gray
    ('90',   'Before Rotation'): '#b03a2e',   # dark red
    ('90',   'After Rotation'):  '#f1948a',   # light red
}

# DPI for saved figures
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
    rel_pos_mm = np.vstack([rel_pos[0], rel_pos[2], -rel_pos[1]]) * 1000  # reorder and scale
    rotated = R @ rel_pos_mm
    return rel_pos_mm, rotated

# ========= MAIN EXECUTION ==========

R = rotation_matrix(rx, ry, rz)
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

# Save data to CSV
box_df = pd.DataFrame(box_data)
stats_df = pd.DataFrame(stats)

box_csv_path = os.path.join(output_dir, 'axis_data_before_after_rotation.csv')
stats_csv_path = os.path.join(output_dir, 'descriptive_stats.csv')

box_df.to_csv(box_csv_path, index=False)
stats_df.to_csv(stats_csv_path, index=False)

print(f"✅ CSV files saved:\n- {box_csv_path}\n- {stats_csv_path}")

# ========= GENERATE AND SAVE BOXPLOTS =========

for axis in ['X', 'Y', 'Z']:
    plt.figure(figsize=(12, 6))
    positions = []
    labels = []
    current_pos = 0

    for dataset in ['Zero', '45', '90']:
        for stage in ['Before Rotation', 'After Rotation']:
            subset = box_df[
                (box_df['Axis'] == axis) &
                (box_df['Dataset'] == dataset) &
                (box_df['Stage'] == stage)
            ]
            color = color_map[(dataset, stage)]

            plt.boxplot(
                subset['Value'],
                positions=[current_pos],
                widths=0.6,
                patch_artist=True,
                boxprops=dict(facecolor=color, color=color),
                medianprops=dict(color='white'),
                whiskerprops=dict(color=color),
                capprops=dict(color=color),
                flierprops=dict(marker='o', markerfacecolor='black', markersize=4, linestyle='none'),
                meanprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=6),
                showmeans=True
            )
            plt.scatter([current_pos]*len(subset), subset['Value'], alpha=0.3, color='black', s=6)
            positions.append(current_pos)
            labels.append(f"{dataset}\n{stage.split()[0]}")
            current_pos += 1

    plt.xticks(positions, labels, fontsize=10)
    plt.xlabel('Dataset and Stage')
    plt.ylabel(f'{axis}-axis (mm)')
    plt.title(f'Boxplot of {axis}-Axis: Original vs. Rotated', fontsize=14)
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()

    output_path = os.path.join(output_dir, f'{axis}_axis_boxplot.png')
    plt.savefig(output_path, dpi=image_dpi)
    print(f"📊 Saved: {output_path}")
    plt.close()

print("✔ All processing complete.")
