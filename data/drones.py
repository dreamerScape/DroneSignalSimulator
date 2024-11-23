drone_data={
    "Orlan-10": {
      "frequency_ranges": [
        {"range_start": "ur_value_in_int", "range_end": "ur_value_in_int"},
        {"range_start": "ur_value_in_int", "range_end": "ur_value_in_int"}
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
  }
  