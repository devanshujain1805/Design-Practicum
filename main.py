'''Importing Modules and Libraries'''

# importing modules
from object_detection import person_detection
from hand_detection import IRsensor

# importing libraries
import RPi.GPIO as GPIO
import time


# setting warnings and output pin
GPIO.setwarnings(False)
output_pin = 18


# detecting objects 
while True:

    #if person and hands both detected...
    if(IRsensor() and person_detection()):

        # the switch will be on
        GPIO.output(output_pin, True)

        #the whole process will take around 40 seconds
        time.sleep(40)

        #then the process will stop
        GPIO.output(output_pin,False)



