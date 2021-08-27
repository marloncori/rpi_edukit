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
        for spin in range(self._minSpeed, speed, self._offset): 
            self.__setMotor(spin, 0, 1)
            sleep(0.05)
            
    def counterclockwise(self, speed):
        for spin in range(self._minSpeed, speed, self._offset):
            self.__setMotor(0, spin, 1)
            sleep(0.05)
        
    def stop(self):
        self._pwm = 0
        self.__setMotor(0, 0, 0)

    def close(self):
        self.__setMotor(0,0,0)
        self.uno.exit()
    
    def _speed_map(self, val, i_min, i_max, o_min, o_max):
        return round(o_min + (o_max - o_min) * ((val - i_min) / (i_max - i_min)))
    
    def _speed_map_abs(self, val, i_min, i_max, o_min, o_max):
        return abs(round(o_min + (o_max - o_min) * ((val - i_min) / (i_max - i_min))))
    
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
        if speedPercent < 0.0:
            self._pwm = self._speed_map_abs(speed, -1.0, 0.0, self._minSpeed, self._maxSpeed)
            self.counterclockwise(self._pwm)
        else:
            self._pwm = self._speed_map(speed, 0.0, 1.0, self._minSpeed, self._maxSpeed)
            self.clockwise(self._pwm)
