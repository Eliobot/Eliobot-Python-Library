# Eliobot robot Library v1.1
# 2023 ELIO, B3 ROBOTICS
#
# Project home:
#   https://eliobot.com
#

#--------------- LIBRARIES IMPORT ---------------#

import time
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import pwmio
import wifi
import json

try:
    with open('config.json', 'r') as file:
        calibration_data = json.load(file)
except OSError:
    calibration_data = {
        'average_max_value': 40000,
        'average_min_value': 10000
    }

# --------------- PINS DECLARATION ---------------#

# Setup the BATTERY voltage sense pin
vbat_voltage = AnalogIn(board.BATTERY)

# Setup the VBUS sense pin
vbus_sense = DigitalInOut(board.VBUS_SENSE)
vbus_sense.direction = Direction.INPUT

# Obstacle input Pins declaration
obstacleInput = [AnalogIn(board.IO4), AnalogIn(board.IO5), AnalogIn(board.IO6), AnalogIn(board.IO7)]

# Line command pin
lineCmd = DigitalInOut(board.IO33)
lineCmd.direction = Direction.OUTPUT

lineInput = [AnalogIn(board.IO10), AnalogIn(board.IO11), AnalogIn(board.IO12), AnalogIn(board.IO13),
             AnalogIn(board.IO14)]

# Line threshhold
threshold = calibration_data['average_min_value'] + (
        calibration_data['average_max_value'] - calibration_data['average_min_value']) / 2

# Motor Driver Pins declaration
AIN1 = pwmio.PWMOut(board.IO36)
AIN2 = pwmio.PWMOut(board.IO38)
BIN1 = pwmio.PWMOut(board.IO35)
BIN2 = pwmio.PWMOut(board.IO37)


# --------------- INTERNAL VOLTAGES ---------------#

# Measure the battery voltage
def get_battery_voltage():
    """Get the approximate battery voltage."""
    # I don't really understand what CP is doing under the hood here for the ADC range & calibration,
    # but the onboard voltage divider for VBAT sense is setup to deliver 1.1V to the ADC based on it's
    # default factory configuration.
    # This forumla should show the nominal 4.2V max capacity (approximately) when 5V is present and the
    # VBAT is in charge state for a 1S LiPo battery with a max capacity of 4.2V
    global vbat_voltage
    return (vbat_voltage.value / 5371)


# Detect if there is a voltage on the USB connector
def get_vbus_present():
    """Detect if VBUS (5V) power source is present"""
    global vbus_sense
    return vbus_sense.value


# --------------- COLORS ---------------#

# Let the rainbow shine
def rgb_color_wheel(wheel_pos):
    """Color wheel to allow for cycling through the rainbow of RGB colors."""
    wheel_pos = wheel_pos % 255

    if wheel_pos < 85:
        return 255 - wheel_pos * 3, 0, wheel_pos * 3
    elif wheel_pos < 170:
        wheel_pos -= 85
        return 0, wheel_pos * 3, 255 - wheel_pos * 3
    else:
        wheel_pos -= 170
        return wheel_pos * 3, 255 - wheel_pos * 3, 0


# --------------- OBSTACLE SENSORS ---------------#

# Get the obstacles sensors value from Left (position 0) to Right (position 3) and back (postion 4)
def getObstacle(obstacle_pos):
    obstacle_pos = obstacle_pos

    value = 0

    value = obstacleInput[obstacle_pos].value

    if value < 10000:
        return True
    else:
        return False


# --------------- MOTORS ---------------#

# Convert the speed from 0 - 100% to 0 - 65535 for pwmio usage
def setSpeed(speedValue):
    # Some filtering to fit the 0-100% range and increasing the minimum value (motors won't spin under 15%)
    if speedValue > 100:
        speedValue = 100
    elif speedValue < 15:
        speedValue += 15

    pwmValue = int((speedValue / 100) * 65535)

    return pwmValue


# Move the robot Forward (0 - 100% speed)
def moveForward(speed=100):
    pwm_value = setSpeed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value


# Move the robot Backward (0 - 100% speed)
def moveBackward(speed=100):
    pwm_value = setSpeed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = pwm_value
    AIN2.duty_cycle = 0
    BIN1.duty_cycle = pwm_value
    BIN2.duty_cycle = 0


# Turn the robot to the Left (0 - 100% speed)
def turnLeft(speed=100):
    pwm_value = setSpeed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = pwm_value
    BIN2.duty_cycle = 0


# turn to the right
def turnRight(speed=100):
    pwm_value = setSpeed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = pwm_value
    AIN2.duty_cycle = 0
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value


# Stop the robot
def motorStop():
    AIN1.duty_cycle = 2 ** 16 - 1
    AIN2.duty_cycle = 2 ** 16 - 1
    BIN1.duty_cycle = 2 ** 16 - 1
    BIN2.duty_cycle = 2 ** 16 - 1


# Slow the robot and stop
def motorSlow():
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = 0
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = 0


# Spin the left wheel forward (0 - 100% speed)
def spinLeftWheelForward(speed=100):
    pwm_value = setSpeed(speed)

    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value


# Spin the left wheel backward (0 - 100% speed)
def spinLeftWheelBackward(speed=100):
    pwm_value = setSpeed(speed)

    BIN1.duty_cycle = pwm_value
    BIN2.duty_cycle = 0


# Spin the right wheel forward (0 - 100% speed)
def spinRightWheelForward(speed=100):
    pwm_value = setSpeed(speed)

    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value


# Spin the right wheel backward (0 - 100% speed)
def spinRightWheelBackward(speed=100):
    pwm_value = setSpeed(speed)

    AIN1.duty_cycle = pwm_value
    AIN2.duty_cycle = 0


# Move the robot forward one step (= approx. 15cm)
def moveOneStep(speed=100):
    pwm_value = setSpeed(speed)
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value
    time.sleep(1)
    motorStop()


# --------------- BUZZER ---------------#

# Buzzer initialisation
def buzzerInit():
    buzzerPin = pwmio.PWMOut(board.IO17, variable_frequency=True)
    return buzzerPin


#play a frequency (in Hertz) for a given time (in seconds)
def playFrequency(frequency, waitTime, volume):
    """Joue une fréquence (en Hertz) pendant une durée donnée (en secondes) avec un volume spécifié."""
    buzzer = buzzerInit()
    buzzer.frequency = round(frequency)
    buzzer.duty_cycle = int(2 ** (0.06 * volume + 9))  # La valeur 32768 correspond à un cycle de service de 50 % pour obtenir une onde carrée.
    time.sleep(waitTime)
    buzzer.deinit()


# Play a note (C, D, E, F, G, A or B) for a given time (in seconds)
def playNote(note, duration, NOTES_FREQUENCIES, volume):
    if note in NOTES_FREQUENCIES:
        frequency = NOTES_FREQUENCIES[note]
        if frequency != 0.1:
            playFrequency(frequency, duration, volume)
        else:
            time.sleep(duration)


# --------------- LINE FOLLOWING ---------------#

# Get the line sensors value from Left (position 0) to Right (position 4)
def getLine(line_pos):
    ambient = 0
    lit = 0
    value = 0

    # Measure reflected IR
    lineCmd.value = True
    time.sleep(0.02)
    lit = lineInput[line_pos].value

    # Measure ambient light
    lineCmd.value = False
    time.sleep(0.02)
    ambient = lineInput[line_pos].value

    # Ambient - Reflected
    value = ambient - lit

    return value


# Example function to follow a black line on white paper
def followLine(speed=100):
    if getLine(2) < threshold:
        moveForward(speed)

    elif getLine(0) < threshold:
        motorStop()
        spinRightWheelForward(speed)

        time.sleep(0.1)

    elif getLine(1) < threshold:
        motorStop()
        spinRightWheelForward(speed)

    elif getLine(3) < threshold:
        motorStop()
        spinLeftWheelForward(speed)

    elif getLine(4) < threshold:
        motorStop()
        spinLeftWheelForward(speed)
        time.sleep(0.1)

    else:
        motorStop()


# Calibrate the line sensors
def calibrateLineSensors():
    time.sleep(1)

    wait_time = 0.5
    num_samples = 5
    max_values = [0] * num_samples
    min_values = [float('inf')] * num_samples

    moveForward(100)
    time.sleep(wait_time)
    motorStop()
    time.sleep(1)
    updateSensorValues(max_values, min_values)

    moveBackward(100)
    time.sleep(wait_time)
    motorStop()
    time.sleep(1)
    updateSensorValues(max_values, min_values)

    moveBackward(100)
    time.sleep(wait_time)
    motorStop()
    time.sleep(1)
    updateSensorValues(max_values, min_values)

    moveForward(100)
    time.sleep(wait_time)
    motorStop()
    time.sleep(1)
    updateSensorValues(max_values, min_values)

    avg_max_value = sum(max_values) / len(max_values)
    avg_min_value = sum(min_values) / len(min_values)

    saveCalibrationData(avg_max_value, avg_min_value)

    print("Calibration completed:")
    print("Average Max value:", avg_max_value)
    print("Average Min value:", avg_min_value)


def updateSensorValues(max_values, min_values):
    for i in range(5):
        current_value = getLine(i)
        max_values[i] = max(max_values[i], current_value)
        min_values[i] = min(min_values[i], current_value)


def saveCalibrationData(avg_max_value, avg_min_value):
    # Create a dictionary to hold the data
    calibration_data = {
        'average_max_value': avg_max_value,
        'average_min_value': avg_min_value
    }

    # Write the dictionary to a file in JSON format
    with open('config.json', 'w') as file:
        json.dump(calibration_data, file)


# --------------- WIFI ---------------#

# Connect to a wifi network
def connectToWifi(ssid, password, webpassword):
    with open('settings.toml', 'w') as f:
        f.write('CIRCUITPY_WIFI_SSID = "' + ssid + '"\n')
        f.write('CIRCUITPY_WIFI_PASSWORD = "' + password + '"\n')
        f.write('CIRCUITPY_WEB_API_PASSWORD = "' + webpassword + '"\n')

    print("Settings saved")
    print("Restart the board to connect to the wifi network")


# Disconnect from the wifi network
def disconnectFromWifi():
    wifi.radio.enabled = False
    while wifi.radio.connected:
        time.sleep(0.1)
    print("Disconnected from wifi")


# Set Eliobot as an access point
def setAccessPoint(ssid, password):
    wifi.radio.enabled = True
    wifi.radio.start_ap(ssid, password)


# Scan for wifi networks
def scanWifiNetworks():
    wifi.radio.enabled = True
    networks = wifi.radio.start_scanning_networks()
    print("Réseaux WiFi disponibles:")
    for network in networks:
        # RSSI to percentage
        MAX_RSSI = -30  # 100% RSSI
        MIN_RSSI = -90  # 0% RSSI
        rssi = max(min(network.rssi, MAX_RSSI), MIN_RSSI)
        percentage = (rssi - MIN_RSSI) / (MAX_RSSI - MIN_RSSI) * 100

        print("SSID:", network.ssid, ", Canal:", network.channel, ", RSSI:", network.rssi, " (", round(percentage),
              "%)")
    wifi.radio.stop_scanning_networks()
    return networks
