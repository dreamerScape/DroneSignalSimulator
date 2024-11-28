from src.drawer import DroneSignalVisualizer
from src.EnhancedDroneSignalGenerator import EnhancedDroneSignalGenerator


# generator = EnhancedDroneSignalGenerator(environment="city")

# generator.set_columns(["Frequency", "RSSI"])  

# generator.generate_signal(
#     "Orlan-10", duration_seconds=60, drone_mode="Telemetry", distance=1000,
#     environment_factors={"urban_loss": 20, "field_loss": 5, "mountain_loss": 10}
# )

visualizer = DroneSignalVisualizer()
visualizer.run()

# Advanced usage with custom parameters
visualizer = DroneSignalVisualizer(
    drone_type="DJI-Mavic",
    duration_seconds=180,
    drone_mode="Navigation",
    distance=1500,
    environment="mountain",
    environment_factors={
        "urban_loss": 30,
        "field_loss": 10,
        "mountain_loss": 20
    }
)
visualizer.run()