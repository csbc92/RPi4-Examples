import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
buzzer=11
GPIO.setup(buzzer, GPIO.OUT)

while True:

    try:
        GPIO.output(buzzer,GPIO.HIGH)
        print ("Beep")
        sleep(0.5) # Delay in seconds
        GPIO.output(buzzer,GPIO.LOW)
        print ("No Beep")
        sleep(0.5)
    except:
        GPIO.output(buzzer,GPIO.LOW)
        quit()

