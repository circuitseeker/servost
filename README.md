# ST3215 Servo Control

This Python library provides control for the ST3215 servo motor using the Waveshare Bus Servo Adapter. It implements the communication protocol for controlling the servo's position, speed, and mode.

## Features

- Position control with speed and time parameters
- Torque enable/disable
- Mode setting (Servo Mode)
- Serial communication with proper checksum calculation
- Continuous movement patterns

## Requirements

- Python 3.x
- pyserial library
- Waveshare Bus Servo Adapter
- ST3215 Servo Motor

## Installation

1. Clone this repository:
```bash
git clone https://github.com/circuitseeker/servost.git
cd servost
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic example of controlling the servo:

```python
from st_servo_test import STServo

# Initialize the servo
st = STServo(port='/dev/ttyACM0', baudrate=1000000)

# Enable torque
st.writeByte(1, 0x28, 1)

# Set to Servo Mode
st.writeByte(1, 0x30, 0)

# Move to position 2048 (center) with 2 second movement time and speed 1000
st.WritePosEx(1, 2048, 2000, 1000)
```

## Position Mapping

- 0: 0 degrees
- 1024: 90 degrees
- 2048: 180 degrees

## License

MIT License 