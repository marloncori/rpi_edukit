#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from edukit_motor import Motor

rightMotor = Motor('d:10:o','d:9:o','d:12:p', offset=30)
leftMotor = Motor('d:8:o','d:7:o','d:6:p', offset=30)
forwardSpeed = 70, backwardSpeed = 60, turnSpeed = 50

def Forward():
    rightMotor.clockwise(forwardSpeed)
    leftMotor.clockwise(forwardSpeed)
        
def Backward():
    rightMotor.counterclockwise(backwardSpeed)
    leftMotor.counterclockwise(backwardSpeed)
        
def StopMotors():
    rightMotor.stop()
    leftMotor.stop()

def Left():
    rightMotor.clockwise(turnSpeed)
    leftMotor.counterclockwise(turnSpeed)

def Right():
    rightMotor.counterclockwise(turnSpeed)
    leftMotor.clockwise(turnSpeed)

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
