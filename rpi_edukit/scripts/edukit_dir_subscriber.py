#! /usr/bin/env python
import rospy
from std_msgs.msg import String
import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

pins = {"pinMotorAforward":10, "pinMotorAbackward":9,
        "pinMotorBforward":8, "pinMotorBbackward":7}

pwm = ["pwmMotorAforwards", "pwmMotorAbackwards",
      "pwmMotorBforwards", "pwmMotorBbackwards"]

Frequency = 20, DutyCycle = 30, Stop = 0

for i in pins:
    gpio.setup(pins[i], gpio.OUT)
    
pwm[0] = gpio.PWM(pins[0], Frequency)
pwm[1] = gpio.PWM(pins[1], Frequency)
pwm[2] = gpio.PWM(pins[2], Frequency)
pwm[3] = gpio.PWM(pins[3], Frequency)
    
def Forward():
    pwm[0:3:2].ChangeDutyCycle(DutyCycle) #first and third list member
    pwm[1:4:2].ChangeDutyCycle(Stop) #second and fourth member
    
def Backward():
    pwm[0:3:2].ChangeDutyCycle(Stop) #first and last third member
    pwm[1:4:2].ChangeDutyCycle(DutyCycle) #second and fourth member
    
def StopMotors():
    for j in pwm:
        pwm[j].ChangeDutyCycle(Stop)

def Left():
    pwm[0:5:3].ChangeDutyCycle(Stop) #first and last list member
    pwm[1:3].ChangeDutyCycle(DutyCycle) #second and third member

def Right():
    pwm[0:5:3].ChangeDutyCycle(DutyCycle) #first and last list member
    pwm[1:3].ChangeDutyCycle(Stop) #second and third member
        
def CommandCallback(command_message):
    command = command_message.data
    if command = 'forwards':
        print('Moving forward')
        Forward()
    elif command = 'backwards':
        print('Moving backward')
        Backward()
    elif command = 'turn right':
        print('Turning right')
        Right()
    elif command = 'turn left':
        print('Turning left.')
        Left()
    else:
        print("Unknown command. Try again")

if __name__ == '__main__':
    try:
        rospy.init_node('driver')
        rospy.Subscriber('command', String, CommandCallback)
        rospy.spin()

    except rospy.ROSInterruptException:
        StopMotors()
        gpio.cleanup()
