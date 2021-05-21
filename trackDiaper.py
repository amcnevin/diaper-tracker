#!/usr/bin/python3


###############################################################################
# Diaper Tracker
# Simple script to detect the pushing of a tactile switch/push button
# Sends a message to Slack Channel with which button at what time
# Release Notes:
# v1: 2019-04-01 - initial script, while loop with if-elif stmts
# v2: 2021-05-20 - added callbacks and events
#
# author: Tony McNevin
#
###############################################################################
import sys, json, requests, datetime, os
import RPi.GPIO as GPIO

# GPIO and Channel setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
WET_CHANNEL = 8
DIRTY_CHANNEL = 10
MIXED_CHANNEL = 16
BOUNCE_TIME=1000

# Slack Integration Webhook
webhook_url = os.environ['DIAPER_TRACKER_HOOK_URL'] 


def track():
    # intentional infinite loop
    while True:
        pass


def get_datetime() -> str:
    """
    obtain the current datetime
    :returns formatted datetime
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_msg(msg: str):
    """
    posts the provided message to the slack webhook
    in the event of an exception, it logs to stdout
    :param: msg to be displayed in slack message
    """
    try:
        requests.post(webhook_url, data=json.dumps({'text': msg}))
    except:
        print(f"attempted to post msg [{msg}]")


def dirty_callback(channel):
    """
    send the appropriate message when the dirty button is pushed
    :param: channel that was activated 
    """
    send_msg(f":poop: Dirty! at {get_datetime()}")

def wet_callback(channel):
    """
    send the appropriate message when the wet button is pushed
    :param: channel that was activated
    """
    send_msg(f":sweat_drops: Wet! at {get_datetime()}")

def mixed_callback(channel):
    """
    send the appropriate message when the mixed button is pushed
    :param: channel that was activated
    """
    send_msg(f":poop: :sweat_drops: Mixed! at {get_datetime()}")


# setup channels
GPIO.setup(WET_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(DIRTY_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MIXED_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# setup event detects and callbacks
GPIO.add_event_detect(WET_CHANNEL, GPIO.RISING, callback=wet_callback, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(DIRTY_CHANNEL, GPIO.RISING, callback=dirty_callback, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(MIXED_CHANNEL, GPIO.RISING, callback=mixed_callback, bouncetime=BOUNCE_TIME)


if __name__ == '__main__':
    track()


