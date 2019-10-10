import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

time.sleep(5)
PWM = GPIO.PWM(11,100)
PWM.start(100)
print("100% duty cycle")
time.sleep(30)
PWM.ChangeDutyCycle(50)
print("50% duty cycle")
time.sleep(30)
PWM.ChangeDutyCycle(20)
print("20% duty cycle")
time.sleep(30)
PWM.ChangeDutyCycle(0)
print("0% duty cycle")
time.sleep(30)
PWM.stop()
GPIO.cleanup()
