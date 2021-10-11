'''Importing Modules and Libraries'''

# importing modules
from object_detection import person_detection
from hand_detection import IRsensor

# importing libraries
import RPi.GPIO as GPIO
import time


# setting warnings and output pin
GPIO.setwarnings(False)
output_pin_dispenser = 18
output_pin_fog = 23
output_pin_dryer = 24
output_pin_exhaust = 38


# detecting objects 
while True:

    #if person and hands both detected...
    if(IRsensor() and person_detection()):

        # the dispenser switch will be on
        GPIO.output(output_pin_dispenser, True)
        
        #this whole process will take around 5 seconds
        time.sleep(5)
        
        # the dispenser will be off
        GPIO.output(output_pin,False)
        
        # fog
        # the fogand exhaust switch will be on
        GPIO.output(output_pin_fog, True)
	GPIO.output(output_pin_exhaust, True)
        
        # this process will take around 25 seconds
        time.sleep(25)
        
        # the fog switch will be off
        GPIO.output(output_pin,False)
        
        #dryer
        #the dryer switch will be on
	GPIO.output(output_pin_dryer, True)
	
	 #these processes will take around 10 seconds
        time.sleep(10)
        
        # the dryer and exhaust switch will be off
        GPIO.output(output_pin,False)
        GPIO.output(output_pin_exhaust, False)
        
  

