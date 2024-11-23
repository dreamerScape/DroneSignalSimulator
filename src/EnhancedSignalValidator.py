from data.drones import drone_data

class EnhancedSignalValidator:
    @staticmethod
    def validate_signal_data(frequency, strength, bandwidth, drone_type):
        """
        Validates the signal data to ensure it adheres to the specifications for the given drone type.
        :param frequency: Signal frequency in MHz.
        :param strength: Signal strength in dBm.
        :param bandwidth: Signal bandwidth in MHz.
        :param drone_type: Type of drone.
        :return: True if the signal data is valid.
        :raises ValueError: If any parameter is outside the allowed range for the drone.
        """
        drone_info = drone_data.get(drone_type)
        if not drone_info:
            raise ValueError(f"Unknown drone type: {drone_type}")

        # Validate frequency
        valid = any(
            freq_range["range_start"] <= frequency <= freq_range["range_end"]
            for freq_range in drone_info["frequency_ranges"]
        )
        if not valid:
            raise ValueError(f"Frequency {frequency} MHz is out of the valid range for {drone_type}.")

        # Validate signal strength
        if strength < drone_info["signal_strength_range"]["min"] or strength > drone_info["signal_strength_range"]["max"]:
            raise ValueError(f"Signal strength {strength} dBm is out of the valid range for {drone_type}.")

        # Validate bandwidth
        if bandwidth not in drone_info["signal_bandwidths"]:
            raise ValueError(f"Bandwidth {bandwidth} MHz is not valid for {drone_type}.")

        # Ensure realistic correlations between bandwidth and strength
        if bandwidth > 5 and strength < -80:
            raise ValueError(f"Wide bandwidth ({bandwidth} MHz) cannot have such low strength ({strength} dBm).")

        # Ensure strength is not unrealistically high
        if strength > -30:
            raise ValueError(f"Signal strength {strength} dBm is too high for this type of signal.")

        return True

    @staticmethod
    def validate_signal_type(signal_type, drone_type):
        """
        Validates the signal type to ensure it is supported by the given drone type.
        :param signal_type: Type of signal ("Telemetry", "Video", "Noise").
        :param drone_type: Type of drone.
        :return: True if the signal type is valid.
        :raises ValueError: If the signal type is not supported by the drone.
        """
        drone_info = drone_data.get(drone_type)
        if not drone_info:
            raise ValueError(f"Unknown drone type: {drone_type}")

        valid_signal_types = drone_info.get("signal_types", ["Telemetry", "Video"])
        if signal_type not in valid_signal_types:
            raise ValueError(f"Signal type {signal_type} is not supported for {drone_type}. Supported types: {valid_signal_types}")

        return True