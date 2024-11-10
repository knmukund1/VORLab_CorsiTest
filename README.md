
# Corsi Task in Virtual Reality

This repository contains code and resources for running a Virtual Reality-based Corsi Task to assess visuospatial working memory, as described in our manuscript titled "Refining the Corsi Block-Tapping Task: Optimizing Accuracy and Precision through Virtual Reality and Dynamic Sequences."

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Experimental Details](#experimental-details)
- [Authors and Acknowledgements](#authors-and-acknowledgements)
- [License](#license)

## Overview
The Corsi Task is a widely used measure of visuospatial working memory. Our VR implementation addresses key factors that affect performance, including recall order, spatial organization of sequences, item permanence, and presence of cues. By utilizing Virtual Reality, we provide a controlled, low-distraction environment to enhance the accuracy of assessments.

## Requirements
- Python 3.10 or later
- Required packages:
  - `tkinter` (for the graphical user interface)
  - `pyautogui`
  - `pyaudio`
  - `Pillow`
  - `Speech Recognition`
  - Additional standard libraries: `time`, `ast`, `functools`, `threading`

Ensure that your system meets these dependencies, and install them if necessary:
```bash
pip install tk pyautogui pyaudio Pillow SpeechRecognition
```

## Setup
1. **Device Requirements**: This task is designed to run with the Oculus Development Kit 1 for VR display. Make sure your device is properly connected and calibrated as described in the manuscript.
2. **Modify Configuration**: Open `Exp_VR_Corsi.py` and update the `task_order` variable as necessary to customize the order of tasks in your experiment.
3. **Calibration**: Position the VR goggles for optimal comfort and visibility. Run the calibration screen at the start of the experiment to ensure correct alignment for each participant.

## Usage
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/VORLab_CorsiTest.git
   cd VORLab_CorsiTest
   ```
2. Modify `task_order` in `Exp_VR_Corsi.py` if needed.
3. Ensure all required packages are installed.
4. Run the main file:
   ```bash
   python Exp_VR_Corsi.py
   ```
   Follow the on-screen instructions to guide the participant through the tasks.

## Experimental Details
The tasks available in this experiment include:
- **Digit Span Task (DST)** - Control task using verbal recall.
- **Free Recall (FR)** - Report the sequence in any recall order.
- **Sequential Recall (SeR)** - Report the sequence in the same order as presented.
- **Sustained Recall (StR)** - All items are visible at once with an indicated order.
- **Temporal Cues (TC)** - Temporal order indicated on each item.
- **Spatial Cues (SC)** - Items appear without a grid background.

Each task type has different sequence organizations, classified as:
- **Structured/Clustered (SC)**
- **Structured/Unclustered (SU)**
- **Unstructured/Clustered (UC)**
- **Unstructured/Unclustered (UU)**

The sequence length adjusts dynamically using a psychophysical staircase method, providing a precise measure of each participant's Corsi span.

## Authors and Acknowledgements
This study was developed by:
- **Krishna Mukunda**, Johns Hopkins University
- **Yuchen Yang**, Johns Hopkins University
- **Carlo De Lillo**, University of Leicester
- **Qadeer Arshad**, University of Leicester
- **Nana Tevzadze**, Johns Hopkins University
- **Amir Kheradmand**, Johns Hopkins University

This work was supported by grants from the National Institute on Deafness and Other Communication Disorders (NIDCD) and the Leon Levy Foundation.

For any questions, please contact **Amir Kheradmand, M.D.** at [akherad@jhu.edu](mailto:akherad@jhu.edu) or Krishna Mukunda [kmukund1@jhu.edu](mailto:kmukund1@jhu.edu).

## License
This project is licensed under the MIT License - see the LICENSE file for details.
