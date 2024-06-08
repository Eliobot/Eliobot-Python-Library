# Eliobot robot Library
# version = '2.1'
# 2023 ELIO SAS
#
# Project home:
#   https://eliobot.com
#

#------------- LIBRARIES IMPORT --------------#

import json
import math
import re
import time
import wifi

#--------------- ELIOBOT CLASS ---------------#


class Eliobot:
    SPACE_BETWEEN_WHEELS = 77.5  # mm
    WHEEL_DIAMETER = 33.5  # mm
    DISTANCE_PER_REVOLUTION = (WHEEL_DIAMETER * math.pi) / 10  # cm

    def __init__(self,
                 AIN1,
                 AIN2,
                 BIN1,
                 BIN2,
                 vBatt_pin,
                 obstacleInput,
                 buzzer,
                 lineInput,
                 lineCmd):
        """
        Initialize Eliobot with the given hardware components.

        Args:
            AIN1: Motor control pin for direction 1 on motor A.
            AIN2: Motor control pin for direction 2 on motor A.
            BIN1: Motor control pin for direction 1 on motor B.
            BIN2: Motor control pin for direction 2 on motor B.
            vBatt_pin: Pin to read battery voltage.
            obstacleInput: List of obstacle sensor inputs.
            buzzer: Buzzer control object.
            lineInput: List of line sensor inputs.
            lineCmd: Line sensor command pin.
        """
        self.AIN1 = AIN1
        self.AIN2 = AIN2
        self.BIN1 = BIN1
        self.BIN2 = BIN2
        self.vBatt_pin = vBatt_pin
        self.obstacleInput = obstacleInput
        self.buzzer = buzzer
        self.lineInput = lineInput
        self.lineCmd = lineCmd

    # --------------- INTERNAL VOLTAGES ---------------#

    def get_battery_voltage(self):
        """
        Get the battery voltage.

        Returns:
            float: The current battery voltage.
        """
        return ((self.vBatt_pin.value / 2 ** 16) * 3.3) * 2

    # --------------- COLORS ---------------#

    @staticmethod
    def rgb_color_wheel(wheel_pos):
        """
        Generate a color from the color wheel based on the given position.

        Args:
            wheel_pos (int): Position on the color wheel (0-255).

        Returns:
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

    # --------------- OBSTACLE SENSORS ---------------#

    def get_obstacle(self, obstacle_pos):
        """
        Check if there is an obstacle in front of the specified sensor.

        Args:
            obstacle_pos (int): The position of the obstacle sensor.

        Returns:
            bool: True if an obstacle is detected, False otherwise.
        """
        value = self.obstacleInput[obstacle_pos].value
        return value < 10000

    # --------------- MOTORS ---------------#

    def repetition_per_second(self):
        """
        Calculate the number of repetitions per second the motor can perform.

        Returns:
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

        Args:
            speed_value (int): Desired speed value (0-100).

        Returns:
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

        Args:
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

        Args:
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

        Args:
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

        Args:
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
        """
        pwm_value = self.set_speed(speed)

        self.BIN1.duty_cycle = 0
        self.BIN2.duty_cycle = pwm_value

    def spin_left_wheel_backward(self, speed=100):
        """
        Spin the left wheel backward.
        """
        pwm_value = self.set_speed(speed)

        self.BIN2.duty_cycle = 0
        self.BIN1.duty_cycle = pwm_value

    def spin_right_wheel_forward(self, speed=100):
        """
        Spin the right wheel forward.
        """
        pwm_value = self.set_speed(speed)

        self.AIN1.duty_cycle = 0
        self.AIN2.duty_cycle = pwm_value

    def spin_right_wheel_backward(self, speed=100):
        """
        Spin the right wheel backward.
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

        Args:
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

        Args:
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

    # --------------- BUZZER ---------------#

    def play_tone(self, frequency, duration, volume):
        """
        Play a tone with a certain frequency, duration, and volume.

        Args:
            frequency (float): Frequency of the tone in Hz.
            duration (float): Duration of the tone in seconds.
            volume (int): Volume of the tone.
        """
        self.buzzer.frequency = round(frequency)
        self.buzzer.duty_cycle = int(2 ** (0.06 * volume + 9))
        time.sleep(duration)
        self.buzzer.duty_cycle = 0

    def play_note(self, note, duration, NOTES_FREQUENCIES, volume):
        """
        Play a note from the notes frequencies dictionary with a certain duration and volume.

        Args:
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

    def play_notes(self, notes: list[tuple[float | None, float]], volume: int = 80) -> None:
        """
        Plays notes on the buzzer.

        Args:
            notes (list): Tuples of frequency in Hz (0|None for silence), duration in seconds.
            volume (int): Volume of the tone. Defaults to 80.
        """
        for freq, duration in notes:
            if freq is None or freq == 0:
                time.sleep(duration)
            else:
                self.play_tone(freq, duration, volume)

    # Convert note letters to semitones offsets from A in the same octave
    NOTE_OFFSETS = {
        "c": -9,
        "c#": -8,
        "d": -7,
        "d#": -6,
        "e": -5,
        "f": -4,
        "f#": -3,
        "g": -2,
        "g#": -1,
        "a": 0,
        "a#": 1,
        "b": 2,
    }

    @staticmethod
    def note_to_frequency(note: int) -> float:
        """
        Converts a note to its frequency in equal temperament.

        A440 (A4) is note 69, like in the MIDI standard. C4 is note 60.

        Args:
            note: Note number in semitones (12 per octave).

        Returns:
            float: Frequency of the note in Hz.
        """
        semitone_ratio = 2 ** (1 / 12)

        return semitone_ratio ** (note - 69) * 440

    @staticmethod
    def read_rtttl(song: str, micro_pause: float = 0.001) -> list[tuple[float | None, float]]:
        """
        Reads notes from an RTTTL string.

        https://en.wikipedia.org/wiki/Ring_Tone_Text_Transfer_Language

        Args:
            song (str): RTTTL string.
            micro_pause (float): Length of pause between notes. Defaults to 0.001

        Returns:
            list: Tuples of frequency in Hz (None for silence) and duration in seconds.
            Play with play_notes()
        """
        song = song.lower()

        # The first part may contain a title
        *_, headers, note_data = song.split(":")

        headers = headers.strip()
        default_duration, default_octave, tempo = headers.split(",")

        default_duration = int(default_duration.strip()[2:])
        default_octave = int(default_octave.strip()[2:])
        tempo = int(tempo.strip()[2:])

        bar_duration = 4 * 60 / tempo

        note_data = note_data.strip().split(",")

        # [(frequency, duration)]
        # frequency=None for a pause
        notes: list[tuple[float | None, float]] = []

        # [0-9]* : Digits (Duration fraction), may be empty
        # [a-gp]#? : a to g (notes), or p (pause), and maybe a #
        # [0-9]* : Digits (Octave), may be empty
        # \.? : A dot, may be empty
        note_re = re.compile(r"([0-9]*)([a-gp]#?)([0-9]*)(\.?)")

        for note_string in note_data:
            note_string = note_string.strip()
            re_match = note_re.match(note_string)

            if re_match is None:
                raise ValueError(
                    f'Expected a note like "[0-9]*[a-gp]#?[0-9]*\\.?"'
                    f' but got "{note_string}" instead.'
                )

            duration_fraction, letter, octave, dot = re_match.groups()

            if duration_fraction == "":
                duration_fraction = default_duration
            else:
                duration_fraction = int(duration_fraction)

            if octave == "":
                octave = default_octave
            else:
                octave = int(octave)

            duration = bar_duration / duration_fraction

            if dot == ".":
                duration *= 1.5

            if letter == "p":
                freq = None  # silence
            else:
                # A4 becomes 48
                # add 21 to reach 69 (value of A4 in MIDI)
                note_value = Eliobot.NOTE_OFFSETS[letter] + octave * 12 + 21
                freq = Eliobot.note_to_frequency(note_value)

            if duration > micro_pause:
                # Normal note
                notes.append((freq, duration - micro_pause))
                if micro_pause > 0:
                    notes.append((None, micro_pause))
            else:
                # Note is too short (or pause too long)
                notes.append((freq, duration))

        return notes

    def play_rtttl(self, song: str, volume: int = 80, micro_pause: float = 0.001) -> None:
        """
        Plays notes from an RTTTL string.

        https://en.wikipedia.org/wiki/Ring_Tone_Text_Transfer_Language

        Args:
            song (str): RTTTL string.
            volume (int): Volume of the tone. Defaults to 80.
            micro_pause (float): Length of pause between notes. Defaults to 0.001.
        """
        notes = Eliobot.read_rtttl(song, micro_pause)
        self.play_notes(notes)

    # --------------- LINE FOLLOWING ---------------#

    def get_line(self, line_pos):
        """
        Get the value of the line sensor at the given position.

        This method calculates the difference between the sensor reading when
        the lineCmd is active (reflective light) and when it is inactive
        (ambient light). This helps in determining the presence of a line.

        Args:
            line_pos (int): The position of the line sensor.

        Returns:
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

        Args:
            threshold (int): The threshold value for line detection.
        """
        speed = 60

        if self.get_line(2) < threshold:
            self.move_forward(speed)

        elif self.get_line(0) < threshold:
            self.motor_stop()
            self.spin_right_wheel_forward(speed)
            time.sleep(0.1)

        elif self.get_line(1) < threshold:
            self.motor_stop()
            self.spin_right_wheel_forward(speed)

        elif self.get_line(3) < threshold:
            self.motor_stop()
            self.spin_left_wheel_forward(speed)

        elif self.get_line(4) < threshold:
            self.motor_stop()
            self.spin_left_wheel_forward(speed)

            time.sleep(0.1)

        else:
            self.motor_stop()

    def calibrate_line_sensors(self):
        """
        Calibrate the line sensors by moving the robot forward and backward,
        collecting maximum and minimum sensor values, and calculating the
        threshold.
        """
        num_samples = 3
        all_values = [[] for _ in range(5)]

        for _ in range(num_samples):
            self.move_one_step("forward", 5)
            time.sleep(1)
            self.update_sensor_values(all_values)

            self.move_one_step("backward", 5)
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

        Args:
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

        Args:
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

        Args:
            data (list): The list of numbers to calculate the median for.

        Returns:
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

    # --------------- WIFI ---------------#

    @staticmethod
    def connect_to_wifi(ssid, password, webpassword):
        """
        Connect to a wifi network.

        Args:
            ssid (str): The SSID of the wifi network.
            password (str): The password of the wifi network.
            webpassword (str): The web API password.
        """
        with open('settings.toml', 'w') as f:
            f.write(f'CIRCUITPY_WIFI_SSID = "{ssid}"\n')
            f.write(f'CIRCUITPY_WIFI_PASSWORD = "{password}"\n')
            f.write(f'CIRCUITPY_WEB_API_PASSWORD = "{webpassword}"\n')

        print("Settings saved")
        print("Restart the board to connect to the wifi network")

    @staticmethod
    def disconnect_from_wifi():
        """
        Disconnect from the wifi network.
        """
        wifi.radio.enabled = False
        while wifi.radio.connected:
            time.sleep(0.1)
        print("Disconnected from wifi")

    @staticmethod
    def set_access_point(ssid, password):
        """
        Set the access point.

        Args:
            ssid (str): The SSID for the access point.
            password (str): The password for the access point.
        """
        wifi.radio.enabled = True
        wifi.radio.start_ap(ssid, password)

    @staticmethod
    def scan_wifi_networks():
        """
        Scan for available wifi networks.

        Returns:
            list: A list of available wifi networks.
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
