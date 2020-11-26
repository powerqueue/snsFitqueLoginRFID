#!/usr/bin/env python

import RPi.GPIO as GPIO
import requests
import uuid
import json as jsn
import sys
import time
import datetime
from datetime import datetime, tzinfo, timedelta
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("Hold a tag near the reader")

class simple_utc(tzinfo):
    def tzname(self,**kwargs):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(hours=-6)

try:
        n = 5
        while n > 0:
          id,text = reader.read()
          print(id)
          print(text)
          #n -= 1
          #time.sleep(5)
          print("Wait until we load the user interface!")
          reqDict = {"LoginID": str(uuid.uuid4()), "MemberID": str(id), "LocationID": "LA-Gunn_CableLatPull-1", "UserName": text, "EfctvStartDt": datetime.utcnow().replace(tzinfo=simple_utc()).isoformat()}
          headers = {'Content-Type': 'application/json'}
          url = 'http://192.168.1.178:3001/fitqueue-login-api/v1/create-login'
          print(jsn.dumps(reqDict))
#         print(r.json())
#         r = requests.post(url, json=jsn.dumps(reqDict), headers=headers)
          response = requests.request("POST", url, headers=headers, data=jsn.dumps(reqDict))
          print("Status code: ", response.status_code)
          print("Printing Entire Post Request")
#         print(r.json())
          print(response.content)
          time.sleep(3)
          print("Ok, ready again. Hold a tag near the reader")

finally:
    GPIO.cleanup()
