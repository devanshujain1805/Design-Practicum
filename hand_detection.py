''' Importing Modules '''

import RPi.GPIO as GPIO
import time


def IRsensor():
    
    ''' Setting the pin '''

    TRIG = 17
    ECHO = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


    ''' Measuring the Distance '''

    while True:
        print(" In progress ....")

        # setting the pins
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, False)
        
        # allow the sensor to warmup,
        print(" allow the sensor to warmup ")
        time.sleep(0.2)

        # setting the output pin
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG,False)

        # calculating start time and end time of pulse
        while GPIO.input(ECHO)==0:
            _start = time.time()
        while GPIO.input(ECHO)==1:
            _end = time.time()

        # calculating pulse duration
        _duration = _end - _start

        # calculating distance and rounding it off
        dist = _duration * 17150
        dist = round (dist, 2)

        # printing distance in cms
        print ( "distance:", dist, "cm" )

        # checking the condition if distance is less than certain criteria
        if(dist<5):
            return 1
        # otherwise 
        else:
            return 0
