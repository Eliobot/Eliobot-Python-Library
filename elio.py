# Eliobot robot Library
# version = '1.1'
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
import busio

#--------------- PINS DECLARATION ---------------#

# Setup the BATTERY voltage sense pin
vbat_voltage = AnalogIn(board.BATTERY)

# Setup the VBUS sense pin
vbus_sense = DigitalInOut(board.VBUS_SENSE)
vbus_sense.direction = Direction.INPUT

# Obstacle input Pins declaration
obstacleCmd = DigitalInOut(board.IO33)
obstacleCmd.direction = Direction.OUTPUT
obstacleInput = [AnalogIn(board.IO4), AnalogIn(board.IO5), AnalogIn(board.IO6), AnalogIn(board.IO7)]

# Line input Pins declaration
lineInput = [AnalogIn(board.IO10), AnalogIn(board.IO11), AnalogIn(board.IO12), AnalogIn(board.IO13), AnalogIn(board.IO14)]
threshold = 45000

# Motor Driver Pins declaration
AIN1 = pwmio.PWMOut(board.IO36)
AIN2 = pwmio.PWMOut(board.IO38)
BIN1 = pwmio.PWMOut(board.IO35)
BIN2 = pwmio.PWMOut(board.IO37)

#--------------- INTERNAL VOLTAGES ---------------#

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



#--------------- COLORS ---------------#

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



#--------------- OBSTACLE SENSORS ---------------#

# Get the obstacles sensors value from Left (position 0) to Right (position 3) and back (postion 4)
def getObstacle(obstacle_pos):
    obstacle_pos = obstacle_pos
    
    value = 0

    value = obstacleInput[obstacle_pos].value

    if value < 10000:
        return True
    else :
        return False



#--------------- MOTORS ---------------#

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
def moveForward(speed = 100):
    pwm_value = setSpeed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value
    
    
# Move the robot Backward (0 - 100% speed)
def moveBackward(speed = 100):
    pwm_value = setSpeed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = pwm_value
    AIN2.duty_cycle = 0
    BIN1.duty_cycle = pwm_value
    BIN2.duty_cycle = 0
    
    
# Turn the robot to the Left (0 - 100% speed)
def turnLeft(speed = 100):
    pwm_value = setSpeed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = pwm_value
    BIN2.duty_cycle = 0
    
    
# turn to the right
def turnRight(speed = 100):
    pwm_value = setSpeed(speed)

    # Faire avancer le robot à la vitesse spécifiée
    AIN1.duty_cycle = pwm_value
    AIN2.duty_cycle = 0
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value
    

# Stop the robot
def motorStop():
    AIN1.duty_cycle = 2**16-1
    AIN2.duty_cycle = 2**16-1
    BIN1.duty_cycle = 2**16-1
    BIN2.duty_cycle = 2**16-1
    
    
# Slow the robot and stop
def motorSlow():
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = 0
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = 0


# Spin the left wheel forward (0 - 100% speed)
def spinLeftWheelForward(speed = 100):
    pwm_value = setSpeed(speed)
 
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value

# Spin the left wheel backward (0 - 100% speed)
def spinLeftWheelBackward(speed = 100):
    pwm_value = setSpeed(speed)
    
    BIN1.duty_cycle = pwm_value
    BIN2.duty_cycle = 0
    
# Spin the right wheel forward (0 - 100% speed)
def spinRightWheelForward(speed = 100):
    pwm_value = setSpeed(speed)
    
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value

# Spin the right wheel backward (0 - 100% speed)
def spinRightWheelBackward(speed = 100):
    pwm_value = setSpeed(speed)
    
    AIN1.duty_cycle = pwm_value
    AIN2.duty_cycle = 0

    
# Move the robot forward one step (= approx. 15cm)
def moveOneStep(speed = 100):
    pwm_value = setSpeed(speed)
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value
    time.sleep(1)
    motorStop()



#--------------- BUZZER ---------------#

# Buzzer initialisation
def buzzerInit():
    buzzerPin = pwmio.PWMOut(board.IO17, variable_frequency=True)
    return buzzerPin
    
    
# Play a frequency (in Hertz) for a given time (in seconds)
def playFrequency(frequency , waitTime, volume):
    buzzer = buzzerInit()
    buzzer.frequency = round(frequency)
    buzzer.duty_cycle = int(2 ** (0.06*volume + 9))  # 32768 value is 50% duty cycle, to get a square wave.
    time.sleep(waitTime)
    buzzer.deinit()


# Play a note (C, D, E, F, G, A or B) for a given time (in seconds)
def playNote(note, duration, NOTES_FREQUENCIES, volume):
  if note in NOTES_FREQUENCIES:
       frequency = NOTES_FREQUENCIES[note]
       if frequency != 0.1:
           playFrequency(frequency , duration, volume)
       else:
           time.sleep(duration)



#--------------- LINE FOLLOWING ---------------#
           
# Get the line sensors value from Left (position 0) to Right (position 4)
def getLine(line_pos):
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


# Example function to follow a black line on white paper
def followLine():
    sensor1_value = getLine(0)
    sensor2_value = getLine(2)
    sensor3_value = getLine(4)

    # Print sensor values
    print(sensor1_value, sensor2_value, sensor3_value)

    # Line following logic
    if sensor2_value < threshold + 1500:
        # Line detected by middle sensor, move forward
        AIN1.duty_cycle = 0
        AIN2.duty_cycle = 65535
        BIN1.duty_cycle = 0
        BIN2.duty_cycle = 65535

    elif sensor1_value < threshold - 9500:
        # Line detected by left sensor, turn left
        AIN1.duty_cycle = 0
        AIN2.duty_cycle = 8000
        BIN1.duty_cycle = 8000
        BIN2.duty_cycle = 0
      

    elif sensor3_value < threshold - 9500:
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
    






