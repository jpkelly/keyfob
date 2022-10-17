#!/usr/bin/env python3

import logging
logging.basicConfig(filename='/home/pi/debug.log', format='%(asctime)s - %(message)s', level=logging.INFO)

from time import sleep  # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

GPIO.setmode(GPIO.BCM)  # Set's GPIO pins to BCM GPIO numbering
GPIO.setwarnings(False)
INPUT_PIN = 4
LED_R = 27
LED_G = 22
LED_B = 23           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(INPUT_PIN, GPIO.IN)  # Set our input pin to be an input
GPIO.setup(LED_R,GPIO.OUT)
GPIO.setup(LED_G,GPIO.OUT)
GPIO.setup(LED_B,GPIO.OUT)
GPIO.output(LED_R,GPIO.LOW)
GPIO.output(LED_G,GPIO.LOW)
GPIO.output(LED_B,GPIO.HIGH)

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="x.x.x.x", # LVTHN x.x.x.x
  help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=9797,
  help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

# Create a function to run when the input is high
def inputHigh(channel):
    print('SENDING START');
    client.send_message("/transportation", "START");
    GPIO.output(LED_B,GPIO.LOW)
    GPIO.output(LED_R,GPIO.HIGH)
    sleep(0.5)
    GPIO.output(LED_B,GPIO.HIGH)
    GPIO.output(LED_R,GPIO.LOW)
    logging.info("Sending to OSC LVTHN")


GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, callback=inputHigh, bouncetime=2000) # Wait for the input to go low, run the function when it does

logging.info("keyfob.service started")

# Start a loop that never ends
while True:
    # print('0');
    # logging.info("beep")
    sleep(1);           # Sleep for a full second before restarting our loop
