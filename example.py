#
# Example of utilisation for Backpack I2C 
#

from Elio import Motors, EyesMatrix, BackpackI2C
import time
import analogio
import pwmio
import board

vBatt_pin = analogio.AnalogIn(board.BATTERY)
AIN1 = pwmio.PWMOut(board.IO36)
AIN2 = pwmio.PWMOut(board.IO38)
BIN1 = pwmio.PWMOut(board.IO35)
BIN2 = pwmio.PWMOut(board.IO37)
motors = Motors(AIN1, AIN2, BIN1, BIN2, vBatt_pin)

cam = BackpackI2C(SCL=board.IO9, SDA=board.IO8)

eyes = EyesMatrix(board.IO2)
eyes.scroll_matrix_text_both_eyes(cam.scan(), (0, 200, 255), 0.02)

counter = 0
score_treshold = 0.6

while True:
    if counter == 0:
        max_detection = {"score": score_treshold, "label": 0}
        counter = 10

    # Read 29 bytes: 1 count byte + up to 7 detections of 4 bytes each
    buf = cam.read(29)
    if buf:
        count = buf[0]
        if 0 < count <= 7:
            for i in range(count):
                offset = 1 + i * 4
                detection = {
                    "x": buf[offset],
                    "y": buf[offset + 1],
                    "score": buf[offset + 2] / 100.0,
                    "label": buf[offset + 3],
                }
                if detection["score"] > max_detection["score"] and detection["label"] == max_detection["label"]:
                    print("Detection :", detection)
                    max_detection = detection

    if max_detection["score"] > score_treshold:
        if max_detection["x"] < 45:
            eyes.set_matrix_logo(eyes.arrowRight, (51, 255, 51))
            motors.turn_left(speed=25)
        elif max_detection["x"] > 55:
            eyes.set_matrix_logo(eyes.arrowLeft, (51, 255, 51))
            motors.turn_right(speed=25)
        else:
            eyes.set_matrix_logo(eyes.emotionThrilled, (51, 255, 51))
            motors.motor_stop()
    else:
        eyes.set_matrix_logo(eyes.emotionKO, (255, 0, 0))
        motors.motor_stop()

    counter -= 1
    time.sleep(0.05)

