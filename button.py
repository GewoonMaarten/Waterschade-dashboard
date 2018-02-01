"""
This file runs the blecon.pl Perl scripts that activates the bluetooth pairing process.
"""

import RPi.GPIO as GPIO
from subprocess import call

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(5, GPIO.FALLING)

#print("hallo")

call(["perl", "application_logic/sensor_controller/blecon.pl"])
