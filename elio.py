
import time
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import pwmio
import busio


# IR_Cmd declaration
ir_cmd_pin = DigitalInOut(board.IO34)

# boot Declaration
boot = DigitalInOut(board.IO0)


# Line led Declaration
lineLed = DigitalInOut(board.IO18)


# RX TX declaration
uart = busio.UART(board.IO43, board.IO44)

#SDA SCL declaration
i2c = busio.I2C(board.IO8, board.IO9)


# header declaration
header_3_pin = DigitalInOut(board.IO2)


# Setup the BATTERY voltage sense pin
vbat_voltage = AnalogIn(board.BATTERY)

# Setup the VBUS sense pin
vbus_sense = DigitalInOut(board.VBUS_SENSE)
vbus_sense.direction = Direction.INPUT

# Obstacle declaration
obstacleCmd = DigitalInOut(board.IO33)
obstacleCmd.direction = Direction.OUTPUT
obstacleInput = [AnalogIn(board.IO4), AnalogIn(board.IO5), AnalogIn(board.IO6), AnalogIn(board.IO7)]

# Line declaration
lineInput = [AnalogIn(board.IO10), AnalogIn(board.IO11), AnalogIn(board.IO12), AnalogIn(board.IO13), AnalogIn(board.IO14)]
threshold = 45000

# Motor declaration
AIN1 = pwmio.PWMOut(board.IO36)
AIN2 = pwmio.PWMOut(board.IO38)
BIN1 = pwmio.PWMOut(board.IO35)
BIN2 = pwmio.PWMOut(board.IO37)
# Helper functions

def buzzerInit():
    buzzer_pin = pwmio.PWMOut(board.IO17, variable_frequency=True)
    return buzzer_pin
    
def set_pixel_power(state):
    """Enable or Disable power to the onboard NeoPixel to either show colour, or to reduce power fro deep sleep."""
    global pixel_power
    pixel_power.value = state
    
def get_battery_voltage():
    """Get the approximate battery voltage."""
    # I don't really understand what CP is doing under the hood here for the ADC range & calibration,
    # but the onboard voltage divider for VBAT sense is setup to deliver 1.1V to the ADC based on it's
    # default factory configuration.
    # This forumla should show the nominal 4.2V max capacity (approximately) when 5V is present and the
    # VBAT is in charge state for a 1S LiPo battery with a max capacity of 4.2V
    global vbat_voltage
    return (vbat_voltage.value / 5371)

def get_vbus_present():
    """Detect if VBUS (5V) power source is present"""
    global vbus_sense
    return vbus_sense.value

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
    
def get_obstacle(obstacle_pos):
    obstacle_pos = obstacle_pos
    
    value = 0

    value = obstacleInput[obstacle_pos].value

    if value < 10000:
        return True
    else :
        return False
    
# converts speed and set it
def set_speed(speed):
    # Convertir la vitesse de 0-100 à 0-65535 pour pwmio
    pwm_value = int((speed / 100) * 65535)

    return pwm_value
#advance robot with speed
def advance(speed):
    # Convertir la vitesse en pourcentage en une valeur de PWM
    pwm_value = set_speed(speed)

    # Faire avancer le robot à la vitesse spécifiée pendant 5 secondes
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value
#back off the robot
def back (speed):
    # Convertir la vitesse en pourcentage en une valeur de PWM
    pwm_value = set_speed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = pwm_value
    AIN2.duty_cycle = 0
    BIN1.duty_cycle = pwm_value
    BIN2.duty_cycle = 0
#turn to the left
def left (speed):
    # Convertir la vitesse en pourcentage en une valeur de PWM
    pwm_value = set_speed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = pwm_value
    BIN2.duty_cycle = 0
# turn to the right
def right (speed):
    # Convertir la vitesse en pourcentage en une valeur de PWM
    pwm_value = set_speed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = pwm_value
    AIN2.duty_cycle = 0
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value
# Stop the robot
def stop ():
    # Arreter le robot
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = 0
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = 0

# turn the left wheel backwards
def left_wheel_back(speed):
    # Convertir la vitesse en pourcentage en une valeur de PWM
    pwm_value = set_speed(speed)
    BIN1.duty_cycle = pwm_value
    time.sleep(1)
# turn the left wheel forwards
def left_wheel_advance(speed):
    # Convertir la vitesse en pourcentage en une valeur de PWM
    pwm_value = set_speed(speed)
    BIN2.duty_cycle = pwm_value
    time.sleep(1)
 
#turn the right wheel backwards
def right_wheel_advance(speed):
    # Convertir la vitesse en pourcentage en une valeur de PWM
    pwm_value = set_speed(speed)
    AIN2.duty_cycle = pwm_value
    time.sleep(1)
#turn the right wheel forwards
def right_wheel_back(speed):
    # Convertir la vitesse en pourcentage en une valeur de PWM
    pwm_value = set_speed(speed)
    AIN1.duty_cycle = pwm_value
    time.sleep(1)
    
#advance the robot of One case (1 case = 15cm)
def oneCase(speed):
    pwm_value = set_speed(speed)
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value
    time.sleep(1)
    stop()
#play a frequency
def playFrequency(buzzer,frequency):
    buzzer = buzzerInit()
    buzzer.frequency = round(frequency)
    buzzer.duty_cycle = 2**15  # 32768 value is 50% duty cycle, a square wave.
#return the value of the color sensor who is past in
def get_line(line_pos):
    ambient = 0
    lit = 0
    value = 0

    # Measure reflected IR
    obstacleCmd.value = True
    time.sleep(0.02)
    lit = lineInput[line_pos].value

    # Measure ambient light
    obstacleCmd.value = False
    time.sleep(0.02)
    ambient = lineInput[line_pos].value

    # Ambient - Reflected
    value = ambient - lit

    return value




def followLine():
    sensor1_value = get_line(0)
    sensor2_value = get_line(2)
    sensor3_value = get_line(4)

    # Print sensor values
    print(sensor1_value, sensor2_value, sensor3_value)

    # Line following logic
    if get_line(2) < threshold + 1500:
        # Line detected by middle sensor, move forward
        AIN1.duty_cycle = 0
        AIN2.duty_cycle = 65535
        BIN1.duty_cycle = 0
        BIN2.duty_cycle = 65535

    elif get_line(0) < threshold - 9500:
        # Line detected by left sensor, turn left
        AIN1.duty_cycle = 0
        AIN2.duty_cycle = 8000
        BIN1.duty_cycle = 8000
        BIN2.duty_cycle = 0
      

    elif get_line(4) < threshold - 9500:
        # Line detected by right sensor, turn right
        AIN1.duty_cycle = 8000
        AIN2.duty_cycle = 0
        BIN1.duty_cycle = 0
        BIN2.duty_cycle = 8000
       
    else:
        # No line detected, reverse at a slower speed
        AIN1.duty_cycle = 8000
        AIN2.duty_cycle = 0
        BIN1.duty_cycle = 8000
        BIN2.duty_cycle = 0
        

    time.sleep(0.1)
    

def play_note(note, duration,NOTES_FREQUENCIES):
  if note in NOTES_FREQUENCIES:
       frequency = NOTES_FREQUENCIES[note]
       if frequency != 0.1:
           buzzer = buzzerInit()
           playFrequency(buzzer, frequency)
           time.sleep(duration)
           buzzer.deinit()
       else:
           time.sleep(duration)



