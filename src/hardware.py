import smbus

class Hardware:

    def __init__(self, i2c_addr=0x18):
        self._i2c_addr = i2c_addr
        self._bus = smbus.SMBus(1)

    def read_temperature(self):
        # Read the temperature register
        temp = self._bus.read_word_data(self._i2c_addr, 0x05)
        
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

if __name__ == '__main__':
    hard = Hardware()
    print(hard.read_temperature())
