# Eliobot Python Library

### Version 2.0
### 2024 - ELIO SAS

#### Project homepage: [https://eliobot.com](https://eliobot.com)

## Introduction

The Eliobot Python library provides functionality to control the Eliobot robot. It leverages libraries like `time`, `board`, `digitalio`, `analogio` and `pwmio` to interact with various hardware components of the robot, including sensors, motors, LEDs, and more.

## Installation

To install the Eliobot Python library, on your Eliobot go to: [https://app.eliobot.com/update/](https://app.eliobot.com/update/) and update Eliobot it will install the latest version of the library.

Or you can download the library and drop it in the `lib` folder of your Eliobot.

## Use the library in your Python code

To use the Eliobot Python library in your Python code, you need to import the `elio` module. Here is an example:

```python
from elio import Eliobot
```

now you can create an instance of the `Eliobot` class and start controlling the robot. Here is an example:

```python
from elio import Eliobot # Import the Eliobot class
import board # Import the board module
import time # Import the time module
import digitalio # Import the digitalio module
import analogio # Import the analogio module
import pwmio # Import the pwmio module

vBatt_pin = analogio.AnalogIn(board.BATTERY) # Battery voltage pin

obstacleInput = [analogio.AnalogIn(pin) for pin in
                 (board.IO4, board.IO5, board.IO6, board.IO7)] # Obstacle sensors

lineCmd = digitalio.DigitalInOut(board.IO33) # Line sensors command pin
lineCmd.direction = digitalio.Direction.OUTPUT # Set the direction of the line command pin

lineInput = [analogio.AnalogIn(pin) for pin in
             (board.IO10, board.IO11, board.IO12, board.IO13, board.IO14)] # Line sensors

AIN1 = pwmio.PWMOut(board.IO36) # Motor A input 1
AIN2 = pwmio.PWMOut(board.IO38) # Motor A input 2
BIN1 = pwmio.PWMOut(board.IO35) # Motor B input 1
BIN2 = pwmio.PWMOut(board.IO37) # Motor B input 2

buzzer = pwmio.PWMOut(board.IO17, variable_frequency=True) # Buzzer

# Create an instance of the Eliobot class
elio = Eliobot(AIN1, AIN2, BIN1, BIN2, vBatt_pin, obstacleInput, buzzer, lineInput, lineCmd)
```

## Documentation

### Attributes

- `AIN1`: Right Motor input 1 (pwmio.PWMOut)
- `AIN2`: Right Motor input 2 (pwmio.PWMOut)
- `BIN1`: Left Motor input 1 (pwmio.PWMOut)
- `BIN2`: Left Motor input 2 (pwmio.PWMOut)
- `vBatt_pin`: Battery voltage pin (analogio.AnalogIn)
- `obstacleInput`: List of obstacle sensors (analogio.AnalogIn)
- `buzzer`: Buzzer (pwmio.PWMOut)
- `lineInput`: List of line sensors (analogio.AnalogIn)
- `lineCmd`: Line sensors command pin (digitalio.DigitalInOut)

