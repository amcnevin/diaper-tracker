#!/usr/bin/python

###############################################################################
# Diaper Tracker
# Simple script to detect the pushing of a tactile switch/push button
# Sends a message to Slack Channel with which button at what time
# 
# author: Tony McNevin, 2019-04-01
#
###############################################################################

import sys, json, requests, datetime, os
import RPi.GPIO as GPIO

sys.stdout.flush()

# Initialize the Board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Establish which GPIO Pins as inputs
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Grab Slack Webhook
webhook_url = os.environ['SLACK_WH']


while True:
	# Button number 1
	if GPIO.input(10) == GPIO.HIGH:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		slack_msg = { 'text': ":poop: Dirty! at %s" % (now) }
		requests.post(webhook_url, data=json.dumps(slack_msg))
		jsonOut = {'datetime': now, 'output': 'dirty' }
		print(json.dumps(jsonOut))

	# Button number 2
	elif GPIO.input(8) == GPIO.HIGH:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		slack_msg = { 'text': ":sweat_drops: Wet! at %s" % (now) }
		requests.post(webhook_url, data=json.dumps(slack_msg))
		jsonOut = {'datetime': now, 'output': 'wet'}
		print(json.dumps(jsonOut))
	# Button number 3
	elif GPIO.input(16) == GPIO.HIGH:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		slack_msg = { 'text': ":poop: :sweat_drops: Mixed! at %s" % (now) }	
		requests.post(webhook_url, data=json.dumps(slack_msg))
		jsonOut = {'datetime': now, 'output': 'mixed'}
		print(json.dumps(jsonOut))
# End
