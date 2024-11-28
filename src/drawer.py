import matplotlib.pyplot as plt
import time
import numpy as np
from src.EnhancedDroneSignalGenerator import EnhancedDroneSignalGenerator

class DroneSignalVisualizer:
    def __init__(self, 
                 drone_type="Orlan-10",
                 duration_seconds=60,
                 drone_mode="Telemetry",
                 distance=1000,
                 environment="city",
                 environment_factors=None):
        # Signal generation parameters
        self.drone_type = drone_type
        self.duration_seconds = duration_seconds
        self.drone_mode = drone_mode
        self.distance = distance
        self.environment = environment
        self.environment_factors = environment_factors or {
            "urban_loss": 20,
            "field_loss": 5,
            "mountain_loss": 10
        }

        # Visualization state
        self.is_paused = False
        self.times = []
        self.freqs = []

        # Setup matplotlib figure and subplots
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        self._setup_plot()
        
        # Initialize signal generator
        self.signal_data_iter = iter(self._signal_data_generator())

    def _setup_plot(self):
        """Initialize plot settings and controls"""
        plt.tight_layout(pad=3.0)
        self.fig.canvas.mpl_connect('key_press_event', self._toggle_pause)
        plt.figtext(0.02, 0.98, "Press SPACE to pause/resume", 
                   fontsize=8, color='gray', style='italic')
        plt.suptitle(f"Drone Signal Analysis - {self.drone_type} - {self.drone_mode}", 
                    fontsize=12, fontweight='bold')

    def _toggle_pause(self, event):
        """Handle pause/resume functionality"""
        if event.key == ' ':  # Space bar
            self.is_paused = not self.is_paused
            status = "Paused" if self.is_paused else "Running"
            plt.suptitle(
                f"Drone Signal Analysis - {self.drone_type} - {time.strftime('%H:%M:%S')} - {status}", 
                fontsize=12, 
                fontweight='bold'
            )
            plt.draw()

    def _update_scatter_plot(self):
        """Update scatter plot (top-left)"""
        self.ax1.clear()
        self.ax1.set_title("Scatter Plot of Signal Data")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Frequency (MHz)")
        self.ax1.scatter(self.times, self.freqs, c=self.freqs, cmap='viridis', s=2)

    def _update_line_plot(self):
        """Update line plot (top-right)"""
        self.ax2.clear()
        self.ax2.set_title("Line Plot of Signal Data")
        self.ax2.set_xlabel("Time (s)")
        self.ax2.set_ylabel("Frequency (MHz)")
        self.ax2.plot(self.times, self.freqs, color='blue', linewidth=1)

    def _update_heatmap(self):
        """Update heatmap (bottom-left)"""
        self.ax3.clear()
        self.ax3.set_title("Signal Data as Heatmap")
        self.ax3.set_xlabel("Time (s)")
        self.ax3.set_ylabel("Frequency (MHz)")
        heatmap_data = np.array([self.times, self.freqs])
        self.ax3.imshow(heatmap_data, aspect='auto', cmap='viridis', interpolation='nearest')

    def _update_waterfall(self):
        """Update waterfall plot (bottom-right)"""
        self.ax4.clear()
        self.ax4.set_title("Waterfall with Blue Vertical Lines")
        self.ax4.set_xlabel("Time (s)")
        self.ax4.set_ylabel("Frequency (MHz)")
        self.ax4.vlines(self.times, 0, self.freqs, color='blue', linewidth=1)

    def _update_frame(self):
        """Update all plots with new data"""
        if not self.is_paused:
            signal = next(self.signal_data_iter)
            self.times.append(signal[0])
            self.freqs.append(signal[1])

        self._update_scatter_plot()
        self._update_line_plot()
        self._update_heatmap()
        self._update_waterfall()

    def _signal_data_generator(self):
        """Generate signal data continuously"""
        while True:  
            generator = EnhancedDroneSignalGenerator(environment=self.environment)
            generator.set_columns(["Frequency", "RSSI"])  

            signal_data = generator.generate_signal(
                self.drone_type,
                duration_seconds=self.duration_seconds,
                drone_mode=self.drone_mode,
                distance=self.distance,
                environment_factors=self.environment_factors
            )
            for signal in signal_data:
                yield signal
                time.sleep(0.1)

    def run(self):
        """Main loop to run the visualization"""
        try:
            while True:
                self._update_frame()
                plt.pause(0.1)
        except KeyboardInterrupt:
            plt.close()
            print("\nVisualization stopped by user")

def main():
    # Example usage with custom parameters
    visualizer = DroneSignalVisualizer(
        drone_type="Orlan-10",
        duration_seconds=120,
        drone_mode="Telemetry",
        distance=2000,
        environment="city",
        environment_factors={
            "urban_loss": 25,
            "field_loss": 8,
            "mountain_loss": 15
        }
    )
    visualizer.run()

if __name__ == "__main__":
    main()