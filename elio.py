# Eliobot robot Library
# version = '3.0'
# 2023 ELIO SAS
#
# Project home:
#   https://eliobot.com
#

#------------- LIBRARIES IMPORT --------------#

import json
import math
import time
import wifi
import adafruit_irremote


#------------- ELIOBOT CLASS --------------#

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
        Calibrate the line sensors by moving the robot forward and backward,
        collecting maximum and minimum sensor values, and calculating the
        threshold.
        """
        num_samples = 3
        all_values = [[] for _ in range(5)]

        for _ in range(num_samples):
            self.motorClass.move_one_step("forward", 5)
            time.sleep(1)
            self.update_sensor_values(all_values)

            self.motorClass.move_one_step("backward", 5)
            time.sleep(1)
            self.update_sensor_values(all_values)

        max_values = [max(sensor_values) for sensor_values in all_values]
        min_values = [min(sensor_values) for sensor_values in all_values]

        avg_max_value = self.calculate_median(max_values)
        avg_min_value = self.calculate_median(min_values)
        threshold = avg_min_value + (avg_max_value - avg_min_value) / 2

        self.save_calibration_data(threshold)

        print("Calibration completed:")
        print("Calculated Threshold:", threshold)

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
    def __init__(self, ir_receiver):
        """
        Initialize the IR remote receiver.

        :param ir_receiver: The IR receiver initialized with adafruit_irremote.IRReceiver
        """

        self.ir_receiver = ir_receiver

    @staticmethod
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
