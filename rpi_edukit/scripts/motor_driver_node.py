import rospy
from geometry_msgs.msg import Twist
from edukit_motor import Motor

class Driver:
    def __init__(self):
        rospy.init_node('driver')
        self._last_received = rospy.get_time()
        self._timeout = rospy.get_param('-timeout', 2)
        self._rate = rospy.get_param('-rate', 10)
        self._maxSpeed = rospy.get_param('-max_speed', 0.5)
        self._wheelBase = rospy.get_param('-wheel_base', 0.091)

        #now assign pins to motors11
        self._rightMotor = Motor('d:10:o','d:9:o','d:12:p')
        self._leftMotor = Motor('d:8:o','d:7:o','d:6:p')

        self._rightSpeedPercent = 0
        self._leftSpeedPercent = 0
        rospy.Subscriber('cmd_vel', Twist, self._vel_received_callback)

    def _vel_received_callback(self, msg):
        self._last_received = rospy.get_time()

        #take both linear and angular velocity from the message
        vl = message.linear.x
        va = message.angular.z

        #calculate both wheel speed in m/s
        rightSpeed = vl + va * self._wheelBase / 2
        leftSpeed = vl - va * self._wheelBase / 2

        #Ideally I could use now the desired wheel speed along with
        #data from wheel speed sensors to come up with the power I need
        #to apply to the wheels. But I will simply convert m/s into percent
        #of max wheel speed instead. This way I will get a duty cycle I can
        #apply to each PWM-controlled motor.
        self._leftSpeedPercent = 100 * leftSpeed / self._maxSpeed
        self._rightSpeedPercent = 100 * rightSpeed / self._maxSpeed

    def cleanup(self):
        self._leftMotor.close()
        self._rightMotor.close()
        
    def run(self):
        rate = rospy.Rate(self._rate)
        while not rospy.is_shutdown():
            delay = rospy.get_time() - self._last_received
            if delay < self._timeout:
                self._leftMotor.move(self._leftSpeedPercent)
                self._rightMotor.move(self._rightSpeedPercent)
            else:
                self._leftMotor.move(0)
                self._rightMotor.move(0)
        rate.sleep()

motor_driver = Driver()

def main():
    motor_driver.run()
    

if __name__ == '__main__':
    try:
          main()
    except rospy.ROSInterruptException:
        rospy.loginfo("User has finished the program").
        print("Shutting down: stopping motors.')
        motor_driver.cleanup()
