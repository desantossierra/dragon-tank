from __future__ import division
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

camera          = (100, 180, 190)            # head up, resting, down
servo_shoulder  = (100, 300, 530)
servo_elbow     = (100, 310, 460)
servo_wrist     = (100, 330, 530)
servo_clamp     = (100, 300, 300)           # open close

distance_shoulder_elbow_cm = 10
distance_shoulder_clamp_cm = 20
shoulder_height_cm = 20


def manual_configuration():
    pwm.set_all_pwm(0, 300)

    servo_id = int(input(f'Please, select the servo id [11-15]: '))
    print(f'Press Q to stop')
    response = ''
    pos = 300
    while response.lower() != 'q':
        pwm.set_pwm(servo_id, 0, pos)
        response = input(f'Current {pos} (i) increase, (d) decrease, (q) quit, (r) reset, (s) servo: ').lower()
        if response == 'i':
            pos += 10
        elif response == 'd':
            pos -= 10
        elif response == 'r':
            pos = 300
        elif response == 's':
            servo_id = int(input(f'Please, select the servo id [11-15]: '))
            pos = 300

def clean_all():
    global pwm
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(50)
    pwm.set_all_pwm(0, 0)
