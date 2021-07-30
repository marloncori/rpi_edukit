pins = {"pinMotorAforward":10, "pinMotorAbackward":9,
        "pinMotorBforward":8, "pinMotorBbackward":7}

#pwmMotorAforwards = "pwmMotorAforwards"
#pwmMotorAbackwards = "pwmMotorAbackwards"
#pwmMotorBforwards = "pwmMotorBforwards"
#pwmMotorBbackwards = "pwmMotorBbackwards"

pwm = []
pwm.append("pwmMotorAforwards")
pwm.append("pwmMotorAbackwards")
pwm.append("pwmMotorBforwards")
pwm.append("pwmMotorBbackwards")
    
Frequency = 20

for i in pins:
    print("pins(", pins[i],",gpio.OUT)")

    for k in range(0,4):
        print(pwm[k], end="")
        pwm[k] = "gpio.PWM(pins[" + str(pins[i]) + "], " + str(Frequency) + ")"
        print(" =", pwm[k])
        #pwm[k] = pwm[k+1]
        #pwm[k+1] = pwm[k+2]
        #pwm[k+2] = pwm[k+3]
        

for l in range(len(pwm)):
    print(pwm[l],", ", end="")
