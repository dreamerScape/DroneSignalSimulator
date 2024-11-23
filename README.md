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

**Create the data directory and add the drones.py file**
  In the root directory of the repository, create a folder named data and inside that folder, create a file named drones.py. This file will contain the data for    the drones, and it should look like this:
  ```python

  # drones.py

drone_data = {
    "Orlan-10": {
        "frequency_ranges": [
            {"range_start": 1000, "range_end": 2000},  # Example frequency range
            {"range_start": 2100, "range_end": 2200}
             ],
        "signal_types": ["Telemetry", "Video"],
        "doppler_shift_rate": 25,
        "frequency_shift_step": 0.2,
        "signal_bandwidths": [2.2, 7, 1, 4.5],
        "signal_strength_range": {"min": -100, "max": -50},
        "motor_model": "T-Motor U8",
        "max_flight_time": 18,
        "max_speed": 150,
        "altitude_limit": 5000,
        "weight": 7.5,
        "dimensions": {
            "length": 2.4,
            "width": 2.4,
            "height": 1.5
        },
        "battery": "LiPo 12S 22,000mAh",
        "operating_temperature": {"min": -20, "max": 40},
        "additional_features": ["Full Autonomous Flight", "RTK GPS"]
    }
    # Add more drones with different configurations if necessary
}
```
**Clone the repository and set up the environment:**

```bash
git clone https://github.com/dreamerScape/DroneSignalSimulator.git
cd DroneSignalSimulator
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
