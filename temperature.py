import smbus
import time
import socket
import json
import datetime

T_SLEEP     = 10
SERVER_IP   = '192.168.1.12'
SERVER_PORT = 7654
I2C_ADDR    = 0x18

bus = smbus.SMBus(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:

    # Read the temperature register
    temp = bus.read_word_data(I2C_ADDR,0x05)
    
    # Note that the upper/lower must be reversed
    upper_byte = temp & 0xFF
    lower_byte = (temp >> 8) & 0xFF
    
    # See page 25 in the datasheet:
    # https://cdn-shop.adafruit.com/datasheets/MCP9808.pdf
    
    # Mask off the threshold bits
    upper_byte = upper_byte & 0x1F
    
    # Handle signs
    if (upper_byte & 0x10) == 0x10:
        upper_byte = upper_byte & 0x0F
        temp = 256-(upper_byte*16+lower_byte/16)
    else:
        temp = upper_byte*16 + lower_byte/16
        
    #print(temp)    
    
    msg = {
        'datetime' : str(datetime.datetime.now()),
        'temp' : temp
        }
   
    sock.sendto(str.encode(json.dumps(msg)), (SERVER_IP,SERVER_PORT))
    
    time.sleep(T_SLEEP)