from src.EnhancedDroneSignalGenerator import EnhancedDroneSignalGenerator


generator = EnhancedDroneSignalGenerator(environment="city")

generator.set_columns(["Time (s)", "Frequency (MHz)", "Signal Strength (dBm)"])  

generator.generate_signal(
    "Orlan-10", duration_seconds=60, drone_mode="Telemetry", distance=1000,
    environment_factors={"urban_loss": 20, "field_loss": 5, "mountain_loss": 30}
)