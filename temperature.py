"""
  - Add this line to /etc/rc.local (before the exit 0):
  -   /home/pi/ONBOOT.sh 2> /home/pi/ONBOOT.errors > /home/pi/ONBOOT.stdout &
  - Add the following ONBOOT.sh script to /home/pi and make it executable:
  
#!/bin/bash
cd /home/pi
python3 temperature.py
  
"""

import smbus
import time
import socket
import json
import datetime

import requests

T_SLEEP  = 60*5
I2C_ADDR = 0x18

post_headers = {
    'X-AIO-Key':' SECRET KEY GOES HERE ', 
    'Content-Type':'application/json'
}

post_url = 'https://io.adafruit.com/api/v2/topher_cantrell/feeds/freezer-temperature/data'

bus = smbus.SMBus(1)

while True:

    # Read the temperature register
    temp = bus.read_word_data(I2C_ADDR,0x05)
    
    # The upper/lower must be reversed    
    upper_byte = temp & 0xFF
    lower_byte = (temp >> 8) & 0xFF    
    temp = (upper_byte << 8) | lower_byte
    
    # See page 25 in the datasheet:
    # https://cdn-shop.adafruit.com/datasheets/MCP9808.pdf
    
    # Hold on to the sign bit (1 means negative)
    tsign = (temp>>12)&1
    
    # 12-bit value / 16
    temp = (temp & 0x0FFF) / 16.0
    if tsign:
        # add in the sign if it is negative
        temp -= 256.0    
              
    #print(temp)    
    
    msg = {
        'created_at' : str(datetime.datetime.now(datetime.timezone.utc).isoformat()),
        'value' : str(temp)
        }
    
    r = requests.post(post_url,data=json.dumps(msg),headers=post_headers)
    #print(r.text)
       
    time.sleep(T_SLEEP)
