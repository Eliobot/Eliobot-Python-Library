# Eliobot Python Library

### Version 3.0 (2023) - ELIO SAS

## Project Homepage
Visit the project homepage at [https://eliobot.com](https://eliobot.com).

## Introduction
The Eliobot Python library provides an extensive set of functionalities to control the Eliobot robot. This library allows you to interact with the robot's motors, sensors, buzzer, and other components using Python.

**Important:** Please note that the IR receiver and the obstacle sensor cannot be used simultaneously because they both share the same pin on the board. You must choose one functionality to use at a time in your code.

## Installation
To install the Eliobot Python library:

1. **Automatic Installation:** Go to [https://app.eliobot.com/update/](https://app.eliobot.com/update/) and update your Eliobot. This will automatically install the latest version of the library.
2. **Manual Installation:** Download the library and place it in the `lib` folder of your Eliobot.

## Documentation
To use the Eliobot Python library in your code, import the necessary modules and create instances of the classes provided:

### Motors Class
Controls the robot's motors.

```python
from elio import Motors
import board
import pwmio
import analogio

vBatt_pin = analogio.AnalogIn(board.BATTERY)
AIN1 = pwmio.PWMOut(board.IO36)
AIN2 = pwmio.PWMOut(board.IO38)
BIN1 = pwmio.PWMOut(board.IO35)
BIN2 = pwmio.PWMOut(board.IO37)

motors = Motors(AIN1, AIN2, BIN1, BIN2, vBatt_pin)
```

#### Methods:
- **move_forward(speed=100)**: Moves the robot forward at the specified speed.
- **move_backward(speed=100)**: Moves the robot backward at the specified speed.
- **turn_left(speed=100)**: Turns the robot left at the specified speed.
- **turn_right(speed=100)**: Turns the robot right at the specified speed.
- **spin_left_wheel_forward(speed=100)**: Spins the left wheel forward.
- **spin_left_wheel_backward(speed=100)**: Spins the left wheel backward.
- **spin_right_wheel_forward(speed=100)**: Spins the right wheel forward.
- **spin_right_wheel_backward(speed=100)**: Spins the right wheel backward.
- **motor_stop()**: Stops the robot immediately.
- **slow_stop()**: Gradually stops the robot.
- **move_one_step(direction, distance=20)**: Moves the robot a specific distance in centimeters.
- **turn_one_step(direction, angle=90)**: Turns the robot a specific angle in degrees.
- **get_battery_voltage()**: Returns the current battery voltage.
- **rgb_color_wheel(wheel_pos)**: Generates a color based on the given position on the color wheel.

### Buzzer Class
Controls the robot's buzzer for sound output.

```python
from elio import Buzzer
import board
import pwmio

buzzer = Buzzer(pwmio.PWMOut(board.IO17, variable_frequency=True))
```

#### Methods:
- **play_tone(frequency, duration, volume)**: Plays a tone with the specified frequency, duration, and volume.
- **play_note(note, duration, NOTES_FREQUENCIES, volume)**: Plays a note from a predefined dictionary of frequencies.

### ObstacleSensor Class
Handles obstacle detection using sensors.

```python
from elio import ObstacleSensor
import board
import analogio

obstacleInput = [analogio.AnalogIn(pin) for pin in 
                 (board.IO4, board.IO5, board.IO6, board.IO7)]

obstacle_sensor = ObstacleSensor(obstacleInput)
```

#### Methods:
- **get_obstacle(obstacle_pos)**: Checks if an obstacle is detected at the specified sensor position.

### LineSensor Class
Manages the line-following capability of the robot.

```python
from elio import LineSensor, Motors
import board
import digitalio
import analogio
import pwmio

vBatt_pin = analogio.AnalogIn(board.BATTERY)

lineCmd = digitalio.DigitalInOut(board.IO33)
lineCmd.direction = digitalio.Direction.OUTPUT

lineInput = [analogio.AnalogIn(pin) for pin in
             (board.IO10, board.IO11, board.IO12, board.IO13, board.IO14)]

AIN1 = pwmio.PWMOut(board.IO36)
AIN2 = pwmio.PWMOut(board.IO38)
BIN1 = pwmio.PWMOut(board.IO35)
BIN2 = pwmio.PWMOut(board.IO37)

motors = Motors(AIN1, AIN2, BIN1, BIN2, vBatt_pin)

lineSensor = LineSensor(lineInput, lineCmd, motors)
```

#### Methods:
- **get_line(line_pos)**: Returns the value of the line sensor at the given position.
- **follow_line(threshold)**: Enables the robot to follow a line based on a threshold value.
- **calibrate_line_sensors()**: Calibrates the line sensors by moving the robot and collecting sensor data.
- **update_sensor_values(all_values)**: Updates sensor readings for calibration purposes.
- **save_calibration_data(threshold)**: Saves the calibration data to a JSON file.
- **calculate_median(data)**: Calculates the median value from a list of numbers.

### WiFiConnectivity Class
Provides WiFi connectivity features for the robot.

```python
from elio import WiFiConnectivity

wifi = WiFiConnectivity()
```

#### Methods:
- **connect_to_wifi(ssid, password, webpassword)**: Connects the robot to a WiFi network.
- **disconnect_from_wifi()**: Disconnects the robot from the WiFi network.
- **set_access_point(ssid, password)**: Sets up the robot as a WiFi access point.
- **scan_wifi_networks()**: Scans for available WiFi networks and displays the results.

### IRRemote Class
Manages the IR remote control functionality.

```python
from elio import IRRemote
import pulseio
import board

ir_receiver = pulseio.PulseIn(board.IO5, maxlen=200, idle_state=True)

ir_remote = IRRemote(ir_receiver)
```

#### Methods:
- **decode_signal()**: Decodes and returns the IR signal received by the IR sensor.

**Important:** Remember that the IR receiver and obstacle sensor share the same pin,
so they cannot be used at the same time.
Ensure that your code only uses one of these features at a time to avoid conflicts.