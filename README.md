# Robotic TEE: LSTM-Based Kinematic Modeling

[![Paper](https://img.shields.io/badge/Paper-Frontiers%20in%20Robotics%20and%20AI-blue)](https://doi.org/10.3389/frobt.2025.1705142)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the code for deep learning-based kinematic modeling of a robotic transesophageal echocardiography (TEE) system.

## Paper

**Robotic transesophageal echocardiography: system design and deep learning-based kinematic modeling**

Seyed MohammadReza Sajadi*, Abbas Tariverdi, Henrik Brun, Ole Jakob Elle, Kim Mathiassen

*Frontiers in Robotics and AI*, 2026

DOI: [10.3389/frobt.2025.1705142](https://doi.org/10.3389/frobt.2025.1705142)

## Abstract

This paper presents a robotic TEE system with deep learning-based kinematic modeling using LSTM networks. The model achieves:
- Position tracking with RMSE below **1.4 mm**
- Mean orientation error of **4.947°** at the clinically critical 90° configuration
- Real-time inference in **1.8 ms**

## Repository Structure
```
├── Dataset_Visualization/     # Scripts for visualizing collected trajectories
│   ├── imge/                  # Visualization outputs
│   └── output_results/        # Statistical analysis results
├── Original_1/                # LSTM model training on original dataset
│   ├── Final_model.ipynb      # Training notebook
│   └── *.h5                   # Trained model weights
├── rotated_2/                 # LSTM model training on rotated dataset
│   ├── Final_model.ipynb      # Training notebook
│   └── *.h5                   # Trained model weights
└── Result_Visualization/      # Scripts for result analysis and plotting
    ├── Original_Result/       # Visualization for original dataset
    └── Rotate_Result/         # Visualization for rotated dataset
```

## Key Features

- LSTM-based kinematic model for cable-driven continuum mechanisms
- Training on 42,000 synchronized pose-command pairs
- Three gastroscope tube configurations (0°, 45°, 90° bends)
- Coordinate frame independence validation

## Requirements
```
python >= 3.8
tensorflow >= 2.0
numpy
scipy
matplotlib
pandas
```

## Installation
```bash
git clone https://github.com/GandalfTech/robotic-TEE-LSTM-kinematics.git
cd robotic-TEE-LSTM-kinematics
pip install -r requirements.txt
```

## Usage

1. **Dataset Visualization**: Explore the `Dataset_Visualization/` folder for trajectory plotting scripts
2. **Model Training**: Open `Original_1/Final_model.ipynb` or `rotated_2/Final_model.ipynb` in Jupyter
3. **Result Analysis**: Use scripts in `Result_Visualization/` to reproduce paper figures

## Citation

If you use this code in your research, please cite:
```bibtex
@article{sajadi2026robotic,
  title={Robotic transesophageal echocardiography: system design and deep learning-based kinematic modeling},
  author={Sajadi, Seyed MohammadReza and Tariverdi, Abbas and Brun, Henrik and Elle, Ole Jakob and Mathiassen, Kim},
  journal={Frontiers in Robotics and AI},
  volume={12},
  pages={1705142},
  year={2026},
  publisher={Frontiers},
  doi={10.3389/frobt.2025.1705142}
}
```

## Acknowledgments

This project received funding from the University of Oslo under the Intelligent Image Guided Surgery (INIUS) project.

We thank GE Healthcare Norway for providing the ultrasound machine and TEE probe for this research.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Seyed MohammadReza Sajadi - smsajadi@ifi.uio.no

Department of Informatics, University of Oslo, Norway
