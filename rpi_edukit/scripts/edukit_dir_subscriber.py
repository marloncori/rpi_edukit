#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from edukit_motor import Motor

rightMotor = Motor('d:10:o','d:9:o','d:12:p', offset=30)
leftMotor = Motor('d:8:o','d:7:o','d:6:p', offset=30)
motorSpeed = 70
rightSpeed = rightMotor._speed_map(motorSpeed, 0, 100, 0, 256)
leftSpeed = leftMotor._speed_map(motorSpeed, 0, 100, 0, 256)

def Forward():
    rightMotor.clockwise(rightSpeed)
    leftMotor.clockwise(leftSpeed)
        
def Backward():
    rightMotor.counterclockwise(rightSpeed)
    leftMotor.counterclockwise(leftSpeed)
        
def StopMotors():
    rightMotor.stop()
    leftMotor.stop()

def Left():
    rightMotor.clockwise(rightSpeed)
    leftMotor.counterclockwise(leftSpeed)

def Right():
    rightMotor.counterclockwise(rightSpeed)
    leftMotor.clockwise(leftSpeed)

def Finish():
    rightMotor.close()
    leftMotor.close()
        
def CommandCallback(command_message):
    command = command_message.data
    if command = 'forwards':
        print('Moving forward...')
        Forward()
    elif command = 'backwards':
        print('Moving backward...')
        Backward()
    elif command = 'turn right':
        print('Turning right.')
        Right()
    elif command = 'turn left':
        print('Turning left.')
        Left()
    else:
        print("Unknown command. Try again")
        StopMotors()
        
if __name__ == '__main__':
    try:
        rospy.init_node('driver')
        rospy.Subscriber('command', String, CommandCallback)
        rospy.spin()

    except rospy.ROSInterruptException:
        Finish()
