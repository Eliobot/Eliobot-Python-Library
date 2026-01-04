# Eliobot robot Library
# version = '4.0'
# CircuitPython = '9.X.X'
#
# 2023 ELIO SAS
#
# Project home:
#   https://eliobot.com
#

# ------------- LIBRARIES IMPORT --------------#

import json
import math
import time
import wifi
import adafruit_irremote
import random
import neopixel
import time

# ------------- ELIOBOT CLASS --------------#

class Motors:
    SPACE_BETWEEN_WHEELS = 77.5  # mm
    WHEEL_DIAMETER = 33.5  # mm
    DISTANCE_PER_REVOLUTION = (WHEEL_DIAMETER * math.pi) / 10  # cm

    def __init__(self, AIN1, AIN2, BIN1, BIN2, vBatt_pin):
        """
        Initialize the motor pins.

        :arg
            AIN1: Motor control pin for direction 1 on motor A.
            AIN2: Motor control pin for direction 2 on motor A.
            BIN1: Motor control pin for direction 1 on motor B.
            BIN2: Motor control pin for direction 2 on motor B.
        """

        self.AIN1 = AIN1
        self.AIN2 = AIN2
        self.BIN1 = BIN1
        self.BIN2 = BIN2
        self.vBatt_pin = vBatt_pin

    def repetition_per_second(self):
        """
        Calculate the number of repetitions per second the motor can perform.

        :return
            float: The number of repetitions per second.
        """
        vBatt = self.get_battery_voltage()
        if vBatt < 2:
            vBatt = 2
        rpm = 20.3 * vBatt
        rps = rpm / 60
        return rps

    @staticmethod
    def set_speed(speed_value):
        """
        Set the speed of the motor.

        :arg
            speed_value (int): Desired speed value (0-100).

        :return
            int: The PWM value corresponding to the desired speed.
        """
        if speed_value > 100:
            speed_value = 100
        elif speed_value < 15:
            speed_value += 15
        pwm_value = int((speed_value / 100) * 65535)
        return pwm_value

    def move_forward(self, speed=100):
        """
        Move the robot forward.

        :arg
            speed (int, optional): Speed of the robot (0-100). Defaults to 100.
        """
        pwm_value = self.set_speed(speed)
        self.AIN1.duty_cycle = 0
        self.BIN1.duty_cycle = 0
        self.AIN2.duty_cycle = pwm_value
        self.BIN2.duty_cycle = pwm_value

    def move_backward(self, speed=100):
        """
        Move the robot backward.

        :arg
            speed (int, optional): Speed of the robot (0-100). Defaults to 100.
        """
        pwm_value = self.set_speed(speed)
        self.AIN2.duty_cycle = 0
        self.BIN2.duty_cycle = 0
        self.AIN1.duty_cycle = pwm_value
        self.BIN1.duty_cycle = pwm_value

    def turn_left(self, speed=100):
        """
        Turn the robot left.

        :arg
            speed (int, optional): Speed of the robot (0-100). Defaults to 100.
        """
        pwm_value = self.set_speed(speed)
        self.AIN1.duty_cycle = 0
        self.BIN2.duty_cycle = 0
        self.AIN2.duty_cycle = pwm_value
        self.BIN1.duty_cycle = pwm_value

    def turn_right(self, speed=100):
        """
        Turn the robot right.

        :arg
            speed (int, optional): Speed of the robot (0-100). Defaults to 100.
        """
        pwm_value = self.set_speed(speed)
        self.AIN2.duty_cycle = 0
        self.BIN1.duty_cycle = 0
        self.AIN1.duty_cycle = pwm_value
        self.BIN2.duty_cycle = pwm_value

    def spin_left_wheel_forward(self, speed=100):
        """
        Spin the left wheel forward.

        :arg
            speed (int, optional): Speed of the wheel (0-100). Defaults to 100.
        """
        pwm_value = self.set_speed(speed)

        self.BIN1.duty_cycle = 0
        self.BIN2.duty_cycle = pwm_value

    def spin_left_wheel_backward(self, speed=100):
        """
        Spin the left wheel backward.

        :arg
            speed (int, optional): Speed of the wheel (0-100). Defaults to 100.
        """
        pwm_value = self.set_speed(speed)

        self.BIN2.duty_cycle = 0
        self.BIN1.duty_cycle = pwm_value

    def spin_right_wheel_forward(self, speed=100):
        """
        Spin the right wheel forward.

        :arg
            speed (int, optional): Speed of the wheel (0-100). Defaults to 100.
        """
        pwm_value = self.set_speed(speed)

        self.AIN1.duty_cycle = 0
        self.AIN2.duty_cycle = pwm_value

    def spin_right_wheel_backward(self, speed=100):
        """
        Spin the right wheel backward.

        :arg
            speed (int, optional): Speed of the wheel (0-100). Defaults to 100.
        """
        pwm_value = self.set_speed(speed)

        self.AIN2.duty_cycle = 0
        self.AIN1.duty_cycle = pwm_value

    def motor_stop(self):
        """
        Stop the robot.
        """
        self.AIN1.duty_cycle = 2 ** 16 - 1
        self.AIN2.duty_cycle = 2 ** 16 - 1
        self.BIN1.duty_cycle = 2 ** 16 - 1
        self.BIN2.duty_cycle = 2 ** 16 - 1

    def slow_stop(self):
        """
        Slowly stop the robot.
        """
        self.AIN1.duty_cycle = 0
        self.AIN2.duty_cycle = 0
        self.BIN1.duty_cycle = 0
        self.BIN2.duty_cycle = 0

    def move_one_step(self, direction, distance=20):
        """
        Move the robot a certain distance.

        :arg
            direction (str): Direction to move ('forward' or 'backward').
            distance (int): Distance to move in centimeters.
        """
        required_rps = distance / self.DISTANCE_PER_REVOLUTION
        required_time = required_rps / self.repetition_per_second()
        pwm_value = 65535

        if direction == "forward":
            self.AIN1.duty_cycle = 0
            self.BIN1.duty_cycle = 0
            self.AIN2.duty_cycle = pwm_value
            self.BIN2.duty_cycle = pwm_value
        elif direction == "backward":
            self.BIN2.duty_cycle = 0
            self.AIN2.duty_cycle = 0
            self.AIN1.duty_cycle = pwm_value
            self.BIN1.duty_cycle = pwm_value

        time.sleep(required_time)
        self.motor_stop()

    def turn_one_step(self, direction, angle=90):
        """
        Turn the robot a certain angle.

        :arg
            direction (str): Direction to turn ('left' or 'right').
            angle (int, optional): Angle to turn in degrees. Defaults to 90.
        """
        gear_ratio = self.SPACE_BETWEEN_WHEELS / self.WHEEL_DIAMETER
        required_time = (angle / (360 * self.repetition_per_second())) * gear_ratio

        if direction == "left":
            self.turn_left()
            time.sleep(required_time)
            self.motor_stop()
        elif direction == "right":
            self.turn_right()
            time.sleep(required_time)
            self.motor_stop()

    def turn_in_place(self, speed=30, direction="left"):
        """
        Turn the robot in place.

        :arg
            speed (int): Speed of the robot (0-100).
            direction (str): Rotation direction ('left' or 'right').
        """
        pwm_value = self.set_speed(speed)

        if direction == "left":
            self.AIN1.duty_cycle = pwm_value
            self.AIN2.duty_cycle = 0
            self.BIN1.duty_cycle = 0
            self.BIN2.duty_cycle = pwm_value
        elif direction == "right":
            self.AIN1.duty_cycle = 0
            self.AIN2.duty_cycle = pwm_value
            self.BIN1.duty_cycle = pwm_value
            self.BIN2.duty_cycle = 0

    # --------------- INTERNAL VOLTAGES ---------------#

    def get_battery_voltage(self):
        """
        Get the battery voltage.

        :return
            float: The current battery voltage.
        """
        return ((self.vBatt_pin.value / 2 ** 16) * 3.3) * 2

    # --------------- COLORS ---------------#

    @staticmethod
    def rgb_color_wheel(wheel_pos):
        """
        Generate a color from the color wheel based on the given position.

        :arg
            wheel_pos (int): Position on the color wheel (0-255).

        :return
            tuple: The RGB values corresponding to the color-wheel position.
        """
        wheel_pos = wheel_pos % 255

        if wheel_pos < 85:
            return 255 - wheel_pos * 3, 0, wheel_pos * 3
        elif wheel_pos < 170:
            wheel_pos -= 85
            return 0, wheel_pos * 3, 255 - wheel_pos * 3
        else:
            wheel_pos -= 170
            return wheel_pos * 3, 255 - wheel_pos * 3, 0


class Buzzer:
    def __init__(self, buzzer):
        """
        Initialize the buzzer.
        :param buzzer: The buzzer initialized with pwmio.PWMOut
        """
        self.buzzer = buzzer

    def play_tone(self, frequency, duration, volume):
        """
        Play a tone with a certain frequency, duration, and volume.

        :arg
            frequency: Frequency of the tone.
            duration: Duration of the tone.
            volume: Volume of the tone.
        """
        self.buzzer.frequency = round(frequency)
        self.buzzer.duty_cycle = int(2 ** (0.06 * volume + 9))
        time.sleep(duration)
        self.buzzer.duty_cycle = 0

    def play_note(self, note, duration, NOTES_FREQUENCIES, volume):
        """
        Play a note from the notes frequencies dictionary with a certain duration and volume.

        :arg
            note (str): Note to play.
            duration (float): Duration of the note in seconds.
            NOTES_FREQUENCIES (dict): Dictionary of notes and their corresponding frequencies.
            volume (int): Volume of the note.
        """
        if note in NOTES_FREQUENCIES:
            frequency = NOTES_FREQUENCIES[note]
            if frequency != 0.1:
                self.play_tone(frequency, duration, volume)
                self.buzzer.duty_cycle = 0
            else:
                time.sleep(duration)

    def sweep(self, start, end, dur, steps=10, pause=0.01):
        """Sweep frequency from start to end over dur seconds in steps.

        Uses `play_tone(..., volume=100)` for consistent duty cycle.
        """
        step_dur = dur / steps
        step_freq = (end - start) / steps
        for i in range(steps):
            self.play_tone(start + step_freq * i, step_dur, 100)
            time.sleep(pause)

    def sound_jump(self):
        self.sweep(600, 1300, 0.2, 12)

    def sound_laser(self):
        self.sweep(1600, 300, 0.15, 10)

    def sound_question(self):
        self.play_tone(900, 0.1, 100)
        self.play_tone(1100, 0.05, 100)
        self.play_tone(700, 0.15, 100)

    def sound_error(self):
        self.play_tone(300, 0.2, 100)
        self.play_tone(250, 0.2, 100)

    def sound_explosion(self):
        for i in range(18):
            f = 1200 - i * 60 + random.randint(-30, 30)
            self.play_tone(f, 0.015, 100)

    def sound_land(self):
        self.sweep(1000, 400, 0.3, 15)
        self.play_tone(200, 0.1, 100)

    def sound_happy(self):
        self.play_tone(1000, 0.05, 100)
        self.play_tone(1300, 0.05, 100)
        self.play_tone(1600, 0.1, 100)
        self.play_tone(1300, 0.05, 100)
        self.play_tone(1700, 0.2, 100)

    def sound_win(self):
        self.play_tone(1000, 0.1, 100)
        self.play_tone(1300, 0.1, 100)
        self.play_tone(1700, 0.15, 100)
        self.play_tone(2000, 0.2, 100)

    def sound_alert(self):
        for i in range(6):
            self.play_tone(1800 if i % 2 == 0 else 1400, 0.05, 100)

    def sound_hello(self):
        self.sweep(900, 1200, 0.15, 5)
        self.play_tone(1100, 0.1, 100)
        self.sweep(1200, 800, 0.15, 5)

    def sound_startup(self):
        self.sweep(500, 1500, 0.3, 12)
        self.play_tone(1800, 0.1, 100)
        self.play_tone(1500, 0.1, 100)

    def sound_bump(self):
        self.play_tone(800, 0.05, 100)
        self.play_tone(500, 0.05, 100)
        self.play_tone(300, 0.15, 100)

    def sound_blink(self):
        self.play_tone(1000, 0.03, 100)
        self.play_tone(1300, 0.03, 100)
        self.play_tone(1600, 0.05, 100)


class ObstacleSensor:
    def __init__(self, obstacleInput):
        """
        Initialize the obstacle sensor.
        :param obstacleInput: The obstacle sensor initialized with analogio.AnalogIn
        """
        self.obstacleInput = obstacleInput

    def get_obstacle(self, obstacle_pos):
        """
        Check if there is an obstacle in front of the specified sensor.

        :arg
            obstacle_pos (int): The position of the obstacle sensor.

        :return
            bool: True if an obstacle is detected, False otherwise.
        """
        value = self.obstacleInput[obstacle_pos].value
        return value < 10000


class LineSensor:
    def __init__(self, lineInput, lineCmd, motorClass):
        """
        Initialize the line sensor.

        :param lineInput: Array of line sensors initialized with analogio.AnalogIn
        :param lineCmd: Led control pin for the line sensor initialized with digitalio.DigitalInOut
        :param motorClass: Motor class initialized with Motors
        """
        self.lineInput = lineInput
        self.lineCmd = lineCmd
        self.motorClass = motorClass

    # --------------- LINE FOLLOWING ---------------#

    def get_line(self, line_pos):
        """
        Get the value of the line sensor at the given position.

        This method calculates the difference between the sensor reading when
        the lineCmd is active (reflective light) and when it is inactive
        (ambient light). This helps in determining the presence of a line.

        :arg
            line_pos (int): The position of the line sensor.

        :return
            int: The value representing the difference between ambient light
            and reflected light, indicating the presence of a line.
        """

        self.lineCmd.value = True
        time.sleep(0.02)
        lit = self.lineInput[line_pos].value

        self.lineCmd.value = False
        time.sleep(0.02)
        ambient = self.lineInput[line_pos].value

        value = ambient - lit
        return value

    def follow_line(self, threshold):
        """
        Follow the line using the line sensors.

        :arg
            threshold (int): The threshold value for line detection.
        """
        speed = 60

        if self.get_line(2) < threshold:
            self.motorClass.move_forward(speed)

        elif self.get_line(0) < threshold:
            self.motorClass.motor_stop()
            self.motorClass.spin_right_wheel_forward(speed)
            time.sleep(0.1)

        elif self.get_line(1) < threshold:
            self.motorClass.motor_stop()
            self.motorClass.spin_right_wheel_forward(speed)

        elif self.get_line(3) < threshold:
            self.motorClass.motor_stop()
            self.motorClass.spin_left_wheel_forward(speed)

        elif self.get_line(4) < threshold:
            self.motorClass.motor_stop()
            self.motorClass.spin_left_wheel_forward(speed)

            time.sleep(0.1)

        else:
            self.motorClass.motor_stop()

    def calibrate_line_sensors(self):
        """
        Calibrate the line sensors by rotating the robot in place,
        collecting maximum and minimum sensor values, and calculating the
        detection threshold. Then, align the robot so that sensor 2 sees the line.
        """
        num_samples = 30
        all_values = [[] for _ in range(5)]

        print("Starting calibration... Place the robot over the line.")

        # Rotate in place and collect sensor values
        for _ in range(num_samples):
            self.motorClass.turn_in_place(speed=30, direction="left")
            time.sleep(0.05)
            self.update_sensor_values(all_values)

        self.motorClass.motor_stop()

        # Extract max and min for each sensor
        max_values = [max(sensor_values) for sensor_values in all_values]
        min_values = [min(sensor_values) for sensor_values in all_values]

        # Compute average max/min and threshold
        avg_max_value = self.calculate_median(max_values)
        avg_min_value = self.calculate_median(min_values)
        threshold = avg_min_value + (avg_max_value - avg_min_value) / 2

        # Save threshold (as before)
        self.save_calibration_data(threshold)

        print("Calibration completed.")
        print("Calculated Threshold:", threshold)
        print("Rotating to align with the line using sensor 2...")

        # Align with the line when sensor 2 sees it
        while True:
            self.motorClass.turn_in_place(speed=10, direction="left")
            time.sleep(0.02)

            center_value = self.get_line(2)

            if center_value < threshold:
                self.motorClass.motor_stop()
                print("Sensor 2 detected the line. Robot aligned.")
                break

    def update_sensor_values(self, all_values):
        """
        Update the maximum and minimum values for the line sensors.

        :arg
            all_values (list of lists): All sensor readings for further filtering.
        """
        for i in range(5):
            current_value = self.get_line(i)
            all_values[i].append(current_value)

        print("All Values:", all_values)

    @staticmethod
    def save_calibration_data(threshold):
        """
        Save the calibration data to a JSON file.

        :arg
            threshold (float): The calculated threshold value for line detection.
        """
        calibration_data = {
            'line_threshold': threshold
        }
        with open('config.json', 'w') as file:
            json.dump(calibration_data, file)

    @staticmethod
    def calculate_median(data):
        """
        Calculate the median of a list of numbers.

        :arg
            data (list): The list of numbers to calculate the median for.

        :return
            float: The median value.
        """
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 1:
            return sorted_data[n // 2]
        else:
            mid1 = sorted_data[n // 2 - 1]
            mid2 = sorted_data[n // 2]
            return (mid1 + mid2) / 2


class WiFiConnectivity:

    def __init__(self):
        """
        WiFi connectivity class for connecting to a wifi network.
        Help with basic wifi operations.
        """
        pass

    @staticmethod
    def connect_to_wifi(ssid, password, webpassword):
        """
        Connect to a wifi network.

        :arg
            ssid (str): The SSID of the WiFi network.
            password (str): The password of the WiFi network.
            webpassword (str): The web API password.
        """
        with open('settings.toml', 'w') as f:
            f.write(f'CIRCUITPY_WIFI_SSID = "{ssid}"\n')
            f.write(f'CIRCUITPY_WIFI_PASSWORD = "{password}"\n')
            f.write(f'CIRCUITPY_WEB_API_PASSWORD = "{webpassword}"\n')
            f.write(f'CIRCUITPY_WEB_API_PORT = 8080')

        print("Settings saved")
        print("Restart the board to connect to the wifi network")

    @staticmethod
    def disconnect_from_wifi():
        """
        Disconnect from the WiFi network.
        """
        wifi.radio.enabled = False
        while wifi.radio.connected:
            time.sleep(0.1)
        print("Disconnected from wifi")

    @staticmethod
    def set_access_point(ssid, password):
        """
        Set the access point.

        :arg
            ssid (str): The SSID for the access point.
            password (str): The password for the access point.
        """

        with open('settings.toml', 'w') as f:
            f.write(f'CIRCUITPY_WEB_API_PORT = 8080')

        wifi.radio.enabled = True
        wifi.radio.start_ap(ssid, password)

    @staticmethod
    def scan_wifi_networks():
        """
        Scan for available WiFi networks.

        :return
            list: A list of available WiFi networks.
        """
        wifi.radio.enabled = True
        networks = wifi.radio.start_scanning_networks()
        print("Réseaux WiFi disponibles:")
        for network in networks:
            MAX_RSSI = -30
            MIN_RSSI = -90
            rssi = max(min(network.rssi, MAX_RSSI), MIN_RSSI)
            percentage = (rssi - MIN_RSSI) / (MAX_RSSI - MIN_RSSI) * 100
            print(f"SSID: {network.ssid}, Canal: {network.channel}, RSSI: {network.rssi} ({round(percentage)}%)")
        wifi.radio.stop_scanning_networks()
        return networks


class IRRemote:
    # Class-level signals so they can be accessed as IRRemote.SIGNALS
    # or IRRemote.signals (alias) from other modules.
    signals = {
        'signal_1': (0, 255, 162, 93),
        'signal_2': (0, 255, 98, 157),
        'signal_3': (0, 255, 226, 29),
        'signal_4': (0, 255, 34, 221),
        'signal_5': (0, 255, 2, 253),
        'signal_6': (0, 255, 194, 61),
        'signal_7': (0, 255, 224, 31),
        'signal_8': (0, 255, 168, 87),
        'signal_9': (0, 255, 144, 111),
        'signal_0': (0, 255, 152, 103),
        'signal_st': (0, 255, 104, 151),
        'signal_ht': (0, 255, 176, 79),
        'signal_up': (0, 255, 24, 231),
        'signal_left': (0, 255, 16, 239),
        'signal_right': (0, 255, 90, 165),
        'signal_down': (0, 255, 74, 181),
        'signal_ok': (0, 255, 56, 199),
    }

    def __init__(self, ir_receiver):
        """
        Initialize the IR remote receiver.

        :param ir_receiver: The IR receiver initialized with adafruit_irremote.IRReceiver
        """

        self.ir_receiver = ir_receiver

    def decode_signal(self):
        """
        Decode the IR signal.

        :return
            int: The decoded IR signal.
        """
        decoder = adafruit_irremote.NonblockingGenericDecode(self.ir_receiver)
        for message in decoder.read():
            if isinstance(message, adafruit_irremote.IRMessage):
                return message.code
            else:
                return None

class EyesMatrix:
    def __init__(self, pin, brightness=0.05):
        """
        Initializes a new instance of the MatrixLED class.

        Args:
        pin (Pin): The pin object from the board module which the NeoPixel LED matrix is connected to.

        Attributes:
        matrix (NeoPixel): An instance of the NeoPixel class to control the LED matrix.
        logo (list of bools): A list representing the LED status (on/off) for displaying the logo.
        """

        self.matrix = neopixel.NeoPixel(pin, 128, brightness=brightness, auto_write=False, pixel_order=neopixel.GRB)

        self.arrowRight = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
        self.arrowLeft = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.arrowUp = [0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0]
        self.arrowDown = [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0]
        self.emotionDizzy = [0,0,1,1,1,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,1,1,0,1,1,0,1,0,0,0,1,0,1,0,1,0,1,0,0,1,1,0,0,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,1,0,1,0,1,1,1,0,0,1,0,1,0,0,0,1,0,1,1,0,0,1,0,1,0,1,1,0,0,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,1,1,0,0]
        self.emotionConfused = [0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
        self.emotionNeutral = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0]
        self.emotionThrilled = [0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0]
        self.emotionTired = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.emotionAmazed = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0]
        self.emotionMusic = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]
        self.emotionLove = [0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0]
        self.emotionKO = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0]
        self.emotionHappy = [0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
        self.emotionSad = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0]
        self.emotionAngry = [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0]


    def set_matrix_colors(self, led_colors):
        """
       Sets the colors of all LEDs in the matrix.

       Args:
       led_colors (list of tuples): A list of RGB tuples where each tuple represents the color for each LED.
       """

        for i, color in enumerate(led_colors):
            if 0 <= i < 128:
                self.matrix[i] = color
        self.matrix.show()

    def clear_matrix(self):
        """
        Turns off all LEDs in the matrix by setting their color to black (0, 0, 0).
        """

        for i in range(128):
            self.matrix[i] = (0, 0, 0)
        self.matrix.show()

    def set_matrix_logo(self, logo, color):
        """
       Displays a logo on the LED matrix.

       Args:
       color (tuple): An RGB tuple specifying the color of the logo.
       logo (list of bools): A list representing the LED status (on/off) for displaying the logo.
       """

        for i, led in enumerate(logo):
            self.matrix[i] = color if led else (0, 0, 0)
        self.matrix.show()

    
    def scroll_matrix_text_both_eyes(self, text, color, speed=0.1):
        """
        Scrolls text across both eyes (two chained 8x8 matrices) from right to left.

        Args:
            text (str): The text to scroll.
            color (tuple): An RGB tuple specifying the color of the text.
            speed (float): Delay between frames in seconds.

        Details:
            Reuses 5x5 character patterns with 1-pixel top margin. The physical layout expects
            the left eye to occupy indices 0..63 (row-major) and the right eye 64..127.
        """

        char_width = 5
        char_height = 5
        left_cols = 8
        gap = 5  # logical gap between matrices (the 'X' columns)
        right_cols = 8
        matrix_width = left_cols + gap + right_cols  # 21 logical columns
        matrix_height = 8
        top_margin = 1
        space = 1

        # Each logical column holds 8 bits for the 8 rows
        extended_matrix = [0] * (len(text) * (char_width + space) + matrix_width)

        # Build bit-columns from 5x5 characters (placed into the logical stream)
        for i, ch in enumerate(text):
            if ch in self.character:
                for r in range(char_height):
                    for c in range(char_width):
                        if self.character[ch][r][c] == 1:
                            col_idx = (i * (char_width + space)) + c + matrix_width
                            bit_pos = top_margin + r
                            extended_matrix[col_idx] |= (1 << bit_pos)

        # Scroll across the combined logical window
        # Logical columns 0..7 -> left matrix physical cols 0..7 (indices 0..63)
        # Logical columns 8..12 -> gap (no physical pixels)
        # Logical columns 13..20 -> right matrix physical cols 0..7 mapped to indices 64..127
        for offset in range(len(extended_matrix)):
            for row in range(matrix_height):
                for col in range(matrix_width):
                    # Map logical column to physical index or None if in gap
                    if col < left_cols:
                        idx = row * 8 + col
                    elif col >= left_cols + gap:
                        # map to right matrix (subtract left+gap to get 0..7)
                        idx = 64 + row * 8 + (col - (left_cols + gap))
                    else:
                        idx = None

                    char_col = col + offset
                    pixel_on = char_col < len(extended_matrix) and (extended_matrix[char_col] & (1 << row))

                    if idx is not None and idx < len(self.matrix):
                        self.matrix[idx] = color if pixel_on else (0, 0, 0)
            self.matrix.show()
            time.sleep(speed)

    def scroll_matrix_text_eye(self, text, color, eye=0, speed=0.1):
        """
        Scrolls text on a single eye (one 8x8 matrix) from right to left.

        Args:
            text (str): The text to scroll.
            color (tuple): An RGB tuple specifying the color of the text.
            eye (int|str): Which eye to use: 0 or 'left' for left eye, 1 or 'right' for right eye.
            speed (float): The delay in seconds between shifts.

        Details:
            Reuses 5x5 character patterns with 1-pixel top margin. The `eye` parameter selects
            whether pixels are written to indices 0..63 (right) or 64..127 (left).
        """

        # normalize eye (robot perspective): 'left' -> 1, 'right' -> 0
        if isinstance(eye, str):
            eye = 1 if eye.lower().startswith('l') else 0

        char_width = 5  # Character width from 5x5 patterns
        char_height = 5  # Character height from 5x5 patterns
        matrix_width = 8  # 8x8 matrix width (logical window)
        matrix_height = 8  # 8x8 matrix height
        top_margin = 1  # 1 pixel margin at top
        space = 1  # Space between characters

        # Create an extended matrix to handle scrolling out
        extended_matrix = [0] * (len(text) * (char_width + space) + matrix_width)

        # Build the matrix for the entire string first
        for i, char in enumerate(text):
            if char in self.character:
                for x in range(char_height):
                    for y in range(char_width):
                        if self.character[char][x][y] == 1:
                            col_idx = (i * (char_width + space)) + y + matrix_width
                            # Place character with top margin
                            bit_pos = top_margin + x
                            extended_matrix[col_idx] |= (1 << bit_pos)

        # Scroll through the extended matrix
        for offset in range(len(extended_matrix)):
            for row in range(matrix_height):  # 8 rows for 8x8 matrix
                for col in range(matrix_width):  # 8 columns for 8x8 matrix
                    if eye == 1:  # left eye
                        idx = 64 + row * matrix_width + col
                    else:
                        idx = row * matrix_width + col

                    char_col = col + offset
                    if char_col < len(extended_matrix) and (extended_matrix[char_col] & (1 << row)):
                        if idx < len(self.matrix):
                            self.matrix[idx] = color
                    else:
                        if idx < len(self.matrix):
                            self.matrix[idx] = (0, 0, 0)
            self.matrix.show()
            time.sleep(speed)

    # 8x8 matrix index mapping
    m_matrix = [
        [ 0,  1,  2,  3,  4,  5,  6,  7],
        [ 8,  9, 10, 11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20, 21, 22, 23],
        [24, 25, 26, 27, 28, 29, 30, 31],
        [32, 33, 34, 35, 36, 37, 38, 39],
        [40, 41, 42, 43, 44, 45, 46, 47],
        [48, 49, 50, 51, 52, 53, 54, 55],
        [56, 57, 58, 59, 60, 61, 62, 63]
    ]


    # 16x8 matrix visualization 
    #               Right Eye                                              Left Eye
    # [  0][  1][  2][  3][  4][  5][  6][  7] X X X X X [ 64][ 65][ 66][ 67][ 68][ 69][ 70][ 71]  
    # [  8][  9][ 10][ 11][ 12][ 13][ 14][ 15] X X X X X [ 72][ 73][ 74][ 75][ 76][ 77][ 78][ 79] 
    # [ 16][ 17][ 18][ 19][ 20][ 21][ 22][ 23] X X X X X [ 80][ 81][ 82][ 83][ 84][ 85][ 86][ 87]    
    # [ 24][ 25][ 26][ 27][ 28][ 29][ 30][ 31] X X X X X [ 88][ 89][ 90][ 91][ 92][ 93][ 94][ 95]  
    # [ 32][ 33][ 34][ 35][ 36][ 37][ 38][ 39] X X X X X [ 96][ 97][ 98][ 99][100][101][102][103]  
    # [ 40][ 41][ 42][ 43][ 44][ 45][ 46][ 47] X X X X X [104][105][106][107][108][109][110][111]  
    # [ 48][ 49][ 50][ 51][ 52][ 53][ 54][ 55] X X X X X [112][113][114][115][116][117][118][119]   
    # [ 56][ 57][ 58][ 59][ 60][ 61][ 62][ 63] X X X X X [120][121][122][123][124][125][126][127] 


    # Character mapping
    character = {
        'A': [[0, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 1, 1, 1, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0]],
        'a': [[0, 0, 0, 0, 0],[0, 1, 1, 1, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 1, 1]],
        'B': [[1, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 1, 1, 0, 0]],
        'b': [[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[1, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 1, 1, 0, 0]],
        'C': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[0, 1, 1, 1, 0]],
        'c': [[0, 0, 0, 0, 0],[0, 1, 1, 1, 0],[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[0, 1, 1, 1, 0]],
        'D': [[1, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[1, 1, 1, 0, 0]],
        'd': [[0, 0, 0, 1, 0],[0, 0, 0, 1, 0],[0, 1, 1, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 1, 0]],
        'E': [[1, 1, 1, 1, 0],[1, 0, 0, 0, 0],[1, 1, 1, 0, 0],[1, 0, 0, 0, 0],[1, 1, 1, 1, 0]],
        'e': [[0, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 1, 1, 1, 0],[1, 0, 0, 0, 0],[0, 1, 1, 1, 0]],
        'F': [[1, 1, 1, 1, 0],[1, 0, 0, 0, 0],[1, 1, 1, 0, 0],[1, 0, 0, 0, 0],[1, 0, 0, 0, 0]],
        'f': [[0, 0, 1, 1, 0],[0, 1, 0, 0, 0],[1, 1, 1, 1, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0]],
        'G': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 0],[1, 0, 1, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 1, 0]],
        'g': [[0, 1, 1, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 1, 0],[0, 0, 0, 1, 0],[0, 1, 1, 0, 0]],
        'H': [[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[1, 1, 1, 1, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0]],
        'h': [[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[1, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0]],
        'I': [[1, 1, 1, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[1, 1, 1, 0, 0]],
        'i': [[0, 1, 0, 0, 0],[0, 0, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0]],
        'J': [[1, 1, 1, 1, 1],[0, 0, 1, 0, 0],[0, 0, 1, 0, 0],[1, 0, 1, 0, 0],[0, 1, 1, 0, 0]],
        'j': [[0, 0, 0, 1, 0],[0, 0, 0, 1, 0],[0, 0, 0, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 0, 0]],
        'K': [[1, 0, 0, 1, 0],[1, 0, 1, 0, 0],[1, 1, 0, 0, 0],[1, 0, 1, 0, 0],[1, 0, 0, 1, 0]],
        'k': [[1, 0, 0, 0, 0],[1, 0, 1, 0, 0],[1, 1, 0, 0, 0],[1, 0, 1, 0, 0],[1, 0, 0, 1, 0]],
        'L': [[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[1, 1, 1, 1, 0]],
        'l': [[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[1, 1, 1, 0, 0]],
        'M': [[1, 0, 0, 0, 1],[1, 1, 0, 1, 1],[1, 0, 1, 0, 1],[1, 0, 0, 0, 1],[1, 0, 0, 0, 1]],
        'm': [[0, 0, 0, 0, 0],[1, 1, 1, 1, 0],[1, 0, 1, 0, 1],[1, 0, 0, 0, 1],[1, 0, 0, 0, 1]],
        'N': [[1, 0, 0, 0, 1],[1, 1, 0, 0, 1],[1, 0, 1, 0, 1],[1, 0, 0, 1, 1],[1, 0, 0, 0, 1]],
        'n': [[0, 0, 0, 0, 0],[1, 1, 1, 0, 0],[1, 0, 1, 0, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0]],
        'O': [[0, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 0, 0]],
        'o': [[0, 0, 0, 0, 0],[0, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 0, 0]],
        'P': [[1, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 1, 1, 0, 0],[1, 0, 0, 0, 0],[1, 0, 0, 0, 0]],
        'p': [[0, 0, 0, 0, 0],[1, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 1, 1, 0, 0],[1, 0, 0, 0, 0]],
        'Q': [[0, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 0, 1, 0, 0],[1, 0, 0, 1, 0],[0, 1, 1, 1, 0]],
        'q': [[0, 0, 0, 0, 0],[0, 1, 1, 0, 0],[1, 0, 0, 1, 0],[0, 1, 1, 1, 0],[0, 0, 0, 1, 0]],
        'R': [[1, 1, 1, 0, 0],[1, 0, 0, 1, 0],[1, 1, 1, 0, 0],[1, 0, 1, 0, 0],[1, 0, 0, 1, 0]],
        'r': [[0, 0, 0, 0, 0],[0, 1, 1, 1, 0],[1, 0, 0, 0, 0],[1, 0, 0, 0, 0],[1, 0, 0, 0, 0]],
        'S': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 0],[0, 1, 1, 0, 0],[0, 0, 0, 1, 0],[1, 1, 1, 0, 0]],
        's': [[0, 0, 0, 0, 0],[0, 0, 1, 1, 0],[0, 1, 0, 0, 0],[0, 0, 1, 0, 0],[1, 1, 0, 0, 0]],
        'T': [[1, 1, 1, 1, 1],[0, 0, 1, 0, 0],[0, 0, 1, 0, 0],[0, 0, 1, 0, 0],[0, 0, 1, 0, 0]],
        't': [[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 1, 1, 0],[0, 1, 0, 0, 0],[0, 0, 1, 1, 1]],
        'U': [[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 0, 0]],
        'u': [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 1, 0]],
        'V': [[1, 0, 0, 0, 1],[1, 0, 0, 0, 1],[0, 1, 0, 1, 0],[0, 1, 0, 1, 0],[0, 0, 1, 0, 0]],
        'v': [[0, 0, 0, 0, 0],[1, 0, 0, 0, 1],[1, 0, 0, 0, 1],[0, 1, 0, 1, 0],[0, 0, 1, 0, 0]],
        'W': [[1, 0, 0, 0, 1],[1, 0, 0, 0, 1],[1, 0, 1, 0, 1],[1, 1, 0, 1, 1],[1, 0, 0, 0, 1]],
        'w': [[0, 0, 0, 0, 0],[1, 0, 0, 0, 1],[1, 0, 1, 0, 1],[1, 1, 0, 1, 1],[0, 1, 0, 0, 1]],
        'X': [[1, 0, 0, 0, 1],[0, 1, 0, 1, 0],[0, 0, 1, 0, 0],[0, 1, 0, 1, 0],[1, 0, 0, 0, 1]],
        'x': [[0, 0, 0, 0, 0],[1, 0, 0, 1, 0],[0, 1, 1, 0, 0],[0, 1, 1, 0, 0],[1, 0, 0, 1, 0]],
        'Y': [[1, 0, 0, 1, 0],[1, 0, 0, 1, 0],[0, 1, 1, 0, 0],[0, 0, 1, 0, 0],[0, 0, 1, 0, 0]],
        'y': [[0, 0, 0, 0, 0],[1, 0, 0, 1, 0],[0, 1, 1, 0, 0],[0, 0, 1, 0, 0],[1, 1, 0, 0, 0]],
        'Z': [[1, 1, 1, 1, 0],[0, 0, 0, 1, 0],[0, 0, 1, 0, 0],[0, 1, 0, 0, 0],[1, 1, 1, 1, 0]],
        'z': [[0, 0, 0, 0, 0],[1, 1, 1, 1, 0],[0, 0, 1, 0, 0],[0, 1, 0, 0, 0],[1, 1, 1, 1, 0]],
        ' ': [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]],
        '?': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 1],[0, 0, 1, 1, 0],[0, 0, 0, 0, 0],[0, 0, 1, 0, 0]],
        '!': [[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 0, 0, 0, 0],[0, 1, 0, 0, 0]],
        ',': [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 1, 0, 0, 0],[1, 0, 0, 0, 0]],
        '.': [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 1, 0]],
        '0': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 1],[1, 0, 0, 1, 1],[1, 0, 1, 0, 1],[0, 1, 1, 1, 0]],
        '1': [[0, 0, 1, 0, 0],[0, 1, 1, 0, 0],[0, 0, 1, 0, 0],[0, 0, 1, 0, 0],[1, 1, 1, 1, 1]],
        '2': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 1],[0, 0, 1, 0, 0],[0, 1, 0, 0, 0],[1, 1, 1, 1, 1]],
        '3': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 1],[0, 0, 1, 1, 0],[1, 0, 0, 0, 1],[0, 1, 1, 1, 0]],
        '4': [[0, 0, 0, 1, 0],[0, 0, 1, 1, 0],[0, 1, 0, 1, 0],[1, 1, 1, 1, 1],[0, 0, 0, 1, 0]],
        '5': [[1, 1, 1, 1, 1],[1, 0, 0, 0, 0],[1, 1, 1, 1, 0],[0, 0, 0, 0, 1],[1, 1, 1, 1, 0]],
        '6': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 0],[1, 1, 1, 1, 0],[1, 0, 0, 0, 1],[0, 1, 1, 1, 0]],
        '7': [[1, 1, 1, 1, 1],[0, 0, 0, 0, 1],[0, 0, 0, 1, 0],[0, 0, 1, 0, 0],[0, 1, 0, 0, 0]],
        '8': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 1],[0, 1, 1, 1, 0],[1, 0, 0, 0, 1],[0, 1, 1, 1, 0]],
        '9': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 1],[0, 1, 1, 1, 1],[0, 0, 0, 0, 1],[0, 1, 1, 1, 0]],
        '-': [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[1, 1, 1, 1, 1],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]],
        '_': [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[1, 1, 1, 1, 1],[0, 0, 0, 0, 0]],
        '/': [[0, 0, 0, 0, 1],[0, 0, 0, 1, 0],[0, 0, 1, 0, 0],[0, 1, 0, 0, 0],[1, 0, 0, 0, 0]],
        '\\':[[1, 0, 0, 0, 0],[0, 1, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 0, 1, 0],[0, 0, 0, 0, 1]],
        '(': [[0, 0, 1, 0, 0],[0, 1, 0, 0, 0],[1, 0, 0, 0, 0],[0, 1, 0, 0, 0],[0, 0, 1, 0, 0]],
        ')': [[0, 0, 1, 0, 0],[0, 0, 0, 1, 0],[0, 0, 0, 1, 0],[0, 0, 0, 1, 0],[0, 0, 1, 0, 0]],
        '[': [[0, 1, 1, 1, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 1, 1, 0]],
        ']': [[0, 1, 1, 1, 0],[0, 0, 0, 1, 0],[0, 0, 0, 1, 0],[0, 0, 0, 1, 0],[0, 1, 1, 1, 0]],
        '@': [[0, 1, 1, 1, 0],[1, 0, 0, 0, 1],[1, 0, 1, 1, 1],[1, 0, 1, 0, 1],[0, 1, 1, 1, 0]],
        '#': [[0, 1, 0, 1, 0],[0, 1, 0, 1, 0],[1, 1, 1, 1, 1],[0, 1, 0, 1, 0],[1, 1, 1, 1, 1]],
        '$': [[0, 1, 1, 1, 1],[1, 0, 1, 0, 0],[0, 1, 1, 1, 0],[0, 0, 1, 0, 1],[1, 1, 1, 1, 0]],
        '\<':[[0, 0, 0, 1, 0],[0, 0, 1, 0, 0],[0, 1, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 0, 1, 0]],
        '\>':[[0, 1, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 0, 1, 0],[0, 0, 1, 0, 0],[0, 1, 0, 0, 0]],
        '=': [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[1, 1, 1, 1, 1],[0, 0, 0, 0, 0],[1, 1, 1, 1, 1]],
        '+': [[0, 0, 0, 0, 0],[0, 0, 1, 0, 0],[0, 1, 1, 1, 0],[0, 0, 1, 0, 0],[0, 0, 0, 0, 0]],
        '*': [[0, 0, 0, 0, 0],[0, 1, 0, 1, 0],[1, 0, 1, 0, 1],[0, 1, 0, 1, 0],[0, 0, 0, 0, 0]],
        '^': [[0, 0, 1, 0, 0],[0, 1, 0, 1, 0],[1, 0, 0, 0, 1],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]],
        '&': [[0, 0, 1, 1, 0],[0, 1, 0, 0, 1],[0, 0, 1, 1, 0],[1, 0, 1, 0, 1],[0, 1, 0, 1, 0]],
        '%': [[1, 0, 0, 0, 1],[0, 0, 0, 1, 0],[0, 0, 1, 0, 0],[0, 1, 0, 0, 0],[1, 0, 0, 0, 1]],
        '|': [[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0],[0, 1, 0, 0, 0]],
        ':': [[0, 0, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 0, 0, 0]],
        ';': [[0, 0, 0, 0, 0],[0, 1, 0, 0, 0],[0, 0, 0, 0, 0],[0, 1, 0, 0, 0],[1, 0, 0, 0, 0]],
        '\'':[[0, 1, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]]
    }

