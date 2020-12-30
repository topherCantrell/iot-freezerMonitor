"""
  - Add this line to /etc/rc.local (before the exit 0):
  -   /home/pi/ONBOOT.sh 2> /home/pi/ONBOOT.errors > /home/pi/ONBOOT.stdout &
  - Add the following ONBOOT.sh script to /home/pi and make it executable:
  
#!/bin/bash
cd /home/pi/home-freezerMonitor
python3 app_monitor.py  
"""

import smbus
import time
import OLD_ez_post

I2C_ADDR = 0x18

bus = smbus.SMBus(1)

def read_temperature():
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
               
    return temp

while True:
    
    readings = []
    for i in range(6):
        # Readings every 10 seconds for one minute
        readings.append(read_temperature())  
        time.sleep(10)   
     
    try:
        OLD_ez_post.post_to_home_gateway('freezer',readings)
    except OSError:
        pass # Ignore connection error in case the server is down temporarily
           
    