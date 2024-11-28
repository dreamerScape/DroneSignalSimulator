import math
import random
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from data.drones import drone_data  # Import drone data
from src.EnhancedSignalValidator import EnhancedSignalValidator  # Validator for generated signal data

class EnhancedDroneSignalGenerator:
    def __init__(self, package_time=0.02, packages_per_second=10, environment="city"):
        """
        Initialization of the drone signal generator.
        :param package_time: Duration of a single data package (in seconds).
        :param packages_per_second: Number of data packages generated per second.
        :param environment: Type of environment ("city", "open_field", "mountains").
        """
        self.package_time = package_time
        self.packages_per_second = packages_per_second
        self.environment = environment  # Environment type (e.g., city, open field)

    def set_columns(self, columns):
        """
        Sets the columns to save in the output CSV file.
        :param columns: List of column names to save.
        """
        available_columns = ["Time (s)", "Frequency", "Bandwidth (MHz)", "RSSI",
                             "Signal Type", "Doppler Shift", "Multipath Effect", "Jamming"]
        invalid_columns = [col for col in columns if col not in available_columns]
        if invalid_columns:
            raise ValueError(f"Invalid columns: {invalid_columns}. Available columns are: {available_columns}")

        self.columns_to_save = columns
        print(f"Columns set to save: {self.columns_to_save}")
    def generate_random_frequency(self, frequency_ranges):
        """
        Generates a random frequency within the specified frequency ranges.
        :param frequency_ranges: List of valid frequency ranges.
        :return: Randomly selected frequency.
        """
        valid_range = random.choice(frequency_ranges)
        freq = round(random.uniform(valid_range["range_start"], valid_range["range_end"]), 2)
        return freq

    def generate_signal_for_bandwidth(self, bandwidth, signal_strength_range, distance, environment_factors):
        """
        Calculates signal strength based on bandwidth, distance, and environmental factors.
        :param bandwidth: Bandwidth of the signal.
        :param signal_strength_range: Minimum and maximum strength of the signal.
        :param distance: Distance between the drone and the receiver.
        :param environment_factors: Environmental factors affecting signal strength.
        :return: Effective signal strength.
        """
        min_strength = signal_strength_range["min"]
        max_strength = signal_strength_range["max"]

        # Path loss formula
        path_loss = 20 * math.log10(distance)
        effective_signal_strength = max(min_strength, max_strength - path_loss)

        # Apply environment-specific losses
        if self.environment == "city":
            effective_signal_strength -= environment_factors["urban_loss"]
        elif self.environment == "open_field":
            effective_signal_strength -= environment_factors["field_loss"]
        elif self.environment == "mountains":
            effective_signal_strength -= environment_factors["mountain_loss"]

        # Minimum signal strength based on bandwidth
        if bandwidth >= 5:
            effective_signal_strength = max(effective_signal_strength, -80)  # Wideband minimum strength
        else:
            effective_signal_strength = max(effective_signal_strength, -100)  # Narrowband minimum strength

        return effective_signal_strength

    def simulate_doppler_shift(self, base_frequency, doppler_shift_rate, time_elapsed, frequency_ranges):
        """
        Simulates Doppler shift and validates frequency.
        :param base_frequency: Initial frequency.
        :param doppler_shift_rate: Rate of frequency change due to Doppler effect.
        :param time_elapsed: Time elapsed since the start of signal generation.
        :param frequency_ranges: List of valid frequency ranges.
        :return: New frequency after Doppler shift.
        """
        doppler_shift = random.uniform(-doppler_shift_rate, doppler_shift_rate)
        new_freq = base_frequency + doppler_shift * time_elapsed

        # Validate frequency and regenerate if out of range
        if not any(freq_range["range_start"] <= new_freq <= freq_range["range_end"] for freq_range in frequency_ranges):
            new_freq = self.generate_random_frequency(frequency_ranges)
        return round(new_freq, 2)

    def simulate_multipath_and_noise(self, signal_data, background_frequencies, jam_probability=0.1):
        """
        Adds multipath reflections and noise to the generated signal.
        :param signal_data: List of signal data points.
        :param background_frequencies: List of background noise frequencies.
        :param jam_probability: Probability of jamming signals.
        :return: Updated signal data with noise and multipath effects.
        """
        multipath_signals = []
        for row in signal_data:
            time, freq, bandwidth, strength, signal_type, doppler_shift, multipath_effect, jamming = row

            # Simulate multipath reflections
            num_reflections = random.randint(1, 5)
            for _ in range(num_reflections):
                delay = random.uniform(0.001, 0.01)
                attenuation = np.random.rayleigh(scale=0.5) * -20  # Rayleigh fading
                phase_shift = random.uniform(0, 2 * math.pi)
                multipath_signals.append([
                    time + delay,
                    freq + random.uniform(-0.2, 0.2),
                    bandwidth,
                    strength + attenuation * math.cos(phase_shift),
                    signal_type,
                    doppler_shift,
                    multipath_effect,
                    jamming
                ])

            # Simulate background noise
            if random.random() < 0.2:
                noise_freq = random.choice(background_frequencies)
                noise_strength = random.uniform(-110, -90)
                multipath_signals.append([time, noise_freq, bandwidth, noise_strength, signal_type, doppler_shift, multipath_effect, jamming])

            # Simulate jamming
            if random.random() < jam_probability:
                jam_strength = random.uniform(-50, -30)
                multipath_signals.append([time, freq, bandwidth, jam_strength, signal_type, doppler_shift, multipath_effect, jamming])

        return signal_data + multipath_signals

    def generate_signal(self, drone_type, duration_seconds=10, drone_mode=None, distance=1000, environment_factors=None):
        """
        Generates signal data for the specified drone type.
        :param drone_type: Type of drone.
        :param duration_seconds: Duration of signal generation (in seconds).
        :param drone_mode: Mode of the drone signal ("Telemetry", "Video").
        :param distance: Distance between the drone and the receiver.
        :param environment_factors: Environmental factors affecting signal properties.
        :return: List of generated signal data points.
        """
        if drone_type not in drone_data:
            raise ValueError(f"Unknown drone type: {drone_type}")

        drone_info = drone_data[drone_type]
        frequency_ranges = drone_info["frequency_ranges"]
        doppler_shift_rate = drone_info["doppler_shift_rate"]
        signal_strength_range = drone_info["signal_strength_range"]
        signal_bandwidths = drone_info["signal_bandwidths"]

        signal_data = []
        start_time = time.time()

        for i in tqdm(range(duration_seconds * self.packages_per_second), desc=f"Generating signal for {drone_type}", ncols=100):
            freq = self.generate_random_frequency(frequency_ranges)
            doppler_shifted_freq = self.simulate_doppler_shift(freq, doppler_shift_rate, i, frequency_ranges)
            bandwidth = random.choice(signal_bandwidths)
            signal_strength = self.generate_signal_for_bandwidth(bandwidth, signal_strength_range, distance, environment_factors)
            signal_type = random.choice(drone_info.get("signal_types", ["Telemetry", "Video"]))

            if drone_mode and signal_type != drone_mode:
                continue

            EnhancedSignalValidator.validate_signal_data(doppler_shifted_freq, signal_strength, bandwidth, drone_type)
            EnhancedSignalValidator.validate_signal_type(signal_type, drone_type)

            signal_data.append([
                round(time.time() - start_time, 2),
                doppler_shifted_freq,
                bandwidth,
                signal_strength,
                signal_type,
                doppler_shifted_freq - freq,
                random.uniform(-10, 10),
                random.uniform(-10, 10)
            ])

            time.sleep(self.package_time)

        # Simulate noise and multipath effects
        signal_data = self.simulate_multipath_and_noise(signal_data, background_frequencies=[2400, 5200, 5800])

        # Save only selected columns to CSV
        df = pd.DataFrame(signal_data, columns=["Time (s)", "Frequency", "Bandwidth (MHz)", "RSSI",
                                                "Signal Type", "Doppler Shift", "Multipath Effect", "Jamming"])
        df_to_save = df[self.columns_to_save]  # Select only specified columns
        df_to_save.to_csv(f"{drone_type}_optimized_signal.csv", index=False)
        print(f"Data for {drone_type} successfully generated and saved to CSV.")
        
        return signal_data
