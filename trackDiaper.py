#!/usr/bin/python3

import sys
import json
import requests
import datetime
import os

webhook_url = os.environ['SLACK_WH']
slack_msg = { 'text': ':poop: Poop!' }

requests.post(webhook_url, data=json.dumps(slack_msg))
