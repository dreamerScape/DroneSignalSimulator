# DroneSignalSimulator

**DroneSignalSimulator** is a Python-based tool for simulating, visualizing, and analyzing drone RF signals. It generates realistic telemetry, video, and jamming signals under various environmental conditions. The project supports real-time visualization with waterfall plots and is ideal for neural network training and RF signal experiments.

---

## Features

- **Realistic Signal Generation**  
  Simulates telemetry, video, and jamming signals with parameters such as Doppler shifts, noise, multipath effects, and signal strength based on environment (city, open fields, mountains).

- **Customizable Environments**  
  Adjust signal properties dynamically by specifying environment factors (urban loss, field attenuation, mountain interference).

- **Real-Time Visualization**  
  Displays RF signal data as scatter plots, line graphs, grids, or waterfall plots with real-time updates.

- **Modular Structure**  
  Includes an extensible architecture for generating specific signal types, such as Electronic Warfare (EW) signals.

- **Neural Network Training Ready**  
  Generates labeled datasets for training AI models to identify and classify drone signals and EW interference.

---

## Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/dreamerScape/DroneSignalSimulator.git
cd DroneSignalSimulator
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
