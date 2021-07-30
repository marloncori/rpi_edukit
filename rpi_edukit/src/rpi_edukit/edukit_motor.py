import RPi.GPIO as rpi

class Motor:
    def __init__(self, fwd_pin, bck_pin):
        rpi.setmode(rpi.BCM)
        rpi.setwarnings(False)

        rpi.setup(fwd_pin, rpi.OUT)
        rpi.setup(bck_pin, rpi.OUT)

        self._FREQ = 20
        self._fwd_pwm = rpi.PWM(fwd_pin, _FREQ)
        self._bck_pwm = rpi.PWM(bck_pin, _FREQ)

    def _clip(value, minim, maxim):
        """Ensure value is between minimum and maximum."""
    
        if value < minim:
            return minim
        elif value > maxim:
            return maxim
        return value
    
    def move(self, speedPercent):
        speed = _clip(abs(speedPercent), 0, 100)
        #positive speed moves wheels forwards, negative - backwards
        if speedPercent < 0:
            self._bck_pwm.start(speed)
            self._fwd_pwm.start(0)
        else:
            self._fwd_pwm.start(speed)
            self._bck_pwm.start(0)
