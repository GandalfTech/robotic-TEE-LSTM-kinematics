import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings

# Suppress duplicate variable name warnings from scipy
warnings.filterwarnings("ignore", category=UserWarning, module="scipy.io.matlab")

# --- Load MATLAB files (make sure they are in the same folder as this script) ---
data_zero = scipy.io.loadmat("Robot_Data_Zero.mat")
data_45 = scipy.io.loadmat("Robot_Data3_45.mat")
data_90 = scipy.io.loadmat("Robot_Data_90F.mat")

# --- Function to extract and transform positions ---
def process_ir_positions(data):
    ir_positions = data['ir_positions']
    ir_positions2 = data['ir_positions2']
    x = ir_positions[0, :] - ir_positions2[0, :]
    y = ir_positions[1, :] - ir_positions2[1, :]
    z = ir_positions[2, :] - ir_positions2[2, :]
    
    # Transform to new coordinate system and convert to millimeters
    X = x * 1000
    Y = z * 1000
    Z = -y * 1000
    return X, Y, Z

# --- Process datasets ---
X0, Y0, Z0 = process_ir_positions(data_zero)
X45, Y45, Z45 = process_ir_positions(data_45)
X90, Y90, Z90 = process_ir_positions(data_90)

# --- Plotting ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 0° Trajectory
ax.plot(X0, Y0, Z0, label='0° Bending (Blue)', color='blue', linewidth=1.2)
ax.scatter(X0, Y0, Z0, c='blue', s=1)

# 45° Trajectory
ax.plot(X45, Y45, Z45, label='45° Bending (Black)', color='black', linewidth=1.2)
ax.scatter(X45, Y45, Z45, c='black', s=1)

# 90° Trajectory
ax.plot(X90, Y90, Z90, label='90° Bending (Magenta)', color='magenta', linewidth=1.2)
ax.scatter(X90, Y90, Z90, c='magenta', s=1)

# Base Marker at origin
ax.scatter(0, 0, 0, color='green', s=100, label='Base Marker', edgecolors='k', marker='o')

# --- Labels, Grid, and View ---
ax.set_xlabel('X (mm)', fontsize=12, fontweight='bold')
ax.set_ylabel('Y (mm)', fontsize=12, fontweight='bold')
ax.set_zlabel('Z (mm)', fontsize=12, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.view_init(elev=25, azim=45)
ax.grid(True)
plt.tight_layout()

# --- Save the plot ---
plt.savefig("bending_visualization.png", dpi=300, bbox_inches='tight')
plt.savefig("bending_visualization.pdf", bbox_inches='tight')
print("✅ Figure saved as 'bending_visualization.png' and 'bending_visualization.pdf'")
