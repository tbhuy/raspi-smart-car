import RPi.GPIO as GPIO
import PCA9685 as PCA
import time
import sys

Motor1In1 = 11
Motor1In2 = 12
Motor2In1 = 13
Motor2In2 = 15
Motor1En = 38
Motor2En = 40
MotorPins = [Motor1In1, Motor1In2, Motor2In1, Motor2In2,Motor1En, Motor2En]
PWM = PCA.PCA9685()
servoPulse = [147,350,589]
#servo_min = 250  # Min pulse length out of 4096
#servo_max = 450  # Max pulse length out of 4096

#servo_mid = (servo_max+servo_min) / 2
servo=len(servoPulse)/2 +1


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
for pin in MotorPins:
    GPIO.setup(pin,GPIO.OUT)

PWM.set_pwm_freq(60)
SpeedMotor1=GPIO.PWM(Motor1En,100)
SpeedMotor2=GPIO.PWM(Motor2En,100)



def run(direction):
    global speed
    direction=int(direction)
    SpeedMotor1.start(speed)
    SpeedMotor2.start(speed)
    if direction == -1:
        GPIO.output(Motor1In1,GPIO.HIGH)
        GPIO.output(Motor1In2,GPIO.LOW)
        GPIO.output(Motor2In1,GPIO.HIGH)
        GPIO.output(Motor2In2,GPIO.LOW)
       
    elif direction == 1:
        GPIO.output(Motor1In1,GPIO.LOW)
        GPIO.output(Motor1In2,GPIO.HIGH)
        GPIO.output(Motor2In1,GPIO.LOW)
        GPIO.output(Motor2In2,GPIO.HIGH)
        
def turn(direction):
    direction=int(direction)
    #global servo, servo_min, servo_max
    global servoPulse, servo
    if direction == 1: #right
        if servo > 0:
           servo -=1
        
        
    elif direction == -1: #left
        if servo < len(servoPulse) -1:
           servo += 1
        
    elif direction == 0: #straight
        servo = len(servoPulse)/2 
    PWM.set_pwm(0, 0, servoPulse[servo])
    time.sleep(0.5)
    PWM.set_pwm(0, 0, 0)
    print >> sys.stdout , servoPulse[servo]

def stop():
    for pin in MotorPins:
        GPIO.output(pin,GPIO.LOW)
    PWM.set_pwm(0, 0, 0)
     
def speedAdjust(step):
    step=int(step)
    global speed
    if step == 1:
        if speed <= 90:
            speed+=10
    elif step == -1:        
        if speed >= 10:
            speed-=10
    SpeedMotor1.start(speed)
    SpeedMotor2.start(speed)
    print >> sys.stdout , speed

speed=50
run(1)
turn(0)
if __name__ == '__main__':
    
    for i in range(1,10):
        run(1)
        turn(1)
        time.sleep(3)
        run(-1)
        turn(-1)
        time.sleep(3)
    stop()

