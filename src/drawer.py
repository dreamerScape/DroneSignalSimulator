import matplotlib.pyplot as plt
import time
import random
import numpy as np
from EnhancedDroneSignalGenerator import EnhancedDroneSignalGenerator


def update_frame(signal_generator, times, freqs, ax1, ax2, ax3, ax4):
    signal = next(signal_generator)
    times.append(signal[0])
    freqs.append(signal[1])

    ax1.clear()
    ax1.set_title("Scatter Plot of Signal Data")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Frequency (MHz)")
    ax1.scatter(times, freqs, c=freqs, cmap='viridis', s=2)

    ax2.clear()
    ax2.set_title("Line Plot of Signal Data")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Frequency (MHz)")
    ax2.plot(times, freqs, color='blue', linewidth=1)

    ax3.clear()
    ax3.set_title("Signal Data as Heatmap")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Frequency (MHz)")
    heatmap_data = np.array([times, freqs])
    ax3.imshow(heatmap_data, aspect='auto', cmap='viridis', interpolation='nearest')

    ax4.clear()
    ax4.set_title("Waterfall with Blue Vertical Lines")
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Frequency (MHz)")
    ax4.vlines(times, 0, freqs, color='blue', linewidth=1)


def signal_data_generator():
    while True:  
        generator = EnhancedDroneSignalGenerator(environment="city")
        signal_data = generator.generate_signal(
            "Orlan-10", duration_seconds=60, drone_mode="Telemetry", distance=1000,
            environment_factors={"urban_loss": 20, "field_loss": 5, "mountain_loss": 30}
        )
        for signal in signal_data:
            yield signal
            time.sleep(0.1)  


def main():
    signal_data_iter = iter(signal_data_generator())

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    ax1.set_title("Scatter Plot of Signal Data")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Frequency (MHz)")

    ax2.set_title("Line Plot of Signal Data")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Frequency (MHz)")

    ax3.set_title("Signal Data as Heatmap")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Frequency (MHz)")

    ax4.set_title("Waterfall with Blue Vertical Lines")
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Frequency (MHz)")

    times = []
    freqs = []

    while True:
        update_frame(signal_data_iter, times, freqs, ax1, ax2, ax3, ax4)
        plt.pause(0.1)  

    # plt.show()

main()