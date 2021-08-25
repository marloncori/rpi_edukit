from pyfirmata import Arduino, util

class Motor(Arduino):

    def __init__(self, positive_pwm, negative_pwm, enable_pwm, minSpeed=0, maxSpeed=100, offset=20):
        self._positive = positive_pwm
        self._negative = negative_pwm
        self._enable = enable_pwm

        self._minSpeed = minSpeed
        self._maxSpeed = maxSpeed
        self._offset = offset
        self._pwm = None
        
        self.uno = Arduino('/dev/ttyACM0')
        self.it = util.Iterator(self.uno)
        self.pinA = self.uno.get_pin(self._positive)
        self.pinB = self.uno.get_pin(self._negative)
        self.pinE = self.uno.get_pin(self._enable)

    def __setMotor(self, fwd_speed, back_speed, state):
        self.pinA.write(fwd_speed)
        self.pinB.write(back_speed)
        self.pinE.write(state)
        
    def clockwise(self, speed):
        self._pwm = speed + 1
        for spin in range(self._minSpeed, self._pwm, self._offset): 
            self.__setMotor(spin, 0, 1)
            sleep(0.04)
            
    def counterclockwise(self, speed):
        self._pwm = speed + 1
        for spin in range(self._minSpeed, self._pwm, self._offset):
            self.__setMotor(0, spin, 1)
            sleep(0.04)
        
    def stop(self):
        self._pwm = 0
        self.__setMotor(self._pwm, self._pwm, 0)

    def close(self):
        self.__setMotor(0,0,0)
        self.uno.exit()
    
    def _speed_map(self, val, i_min, i_max, o_min, o_max):
        self._pwm = round(o_min + (o_max - o_min) * ((val - i_min) / (i_max - i_min)))
        return self._pwm
    
    def _speed_map_abs(self, val, i_min, i_max, o_min, o_max):
        self._pwm = abs(round(o_min + (o_max - o_min) * ((val - i_min) / (i_max - i_min))))
        return self._pwm
    
    def _clip(self, value, minim, maxim):
        #Ensure value is between minimum and maximum.
        if value < minim:
            return minim
        elif value > maxim:
            return maxim
        return value
    
    def move(self, speedPercent):
        speed = self._clip(abs(speedPercent), self._minSpeed, self._maxSpeed)
        #positive speed moves wheels forwards, negative - backwards
        if speedPercent < 0:
            self._speed_map_abs(speed, self._minSpeed, self._maxSpeed, 0, 256)
            self.counterclockwise(speed)
        else:
            self._speed_map(speed, self._minSpeed, self._maxSpeed, 0, 256)
            self.clockwise(speed)
