# Freezer Monitor


## Links

https://learn.adafruit.com/adafruit-mcp9808-precision-i2c-temperature-sensor-guide

https://cdn-shop.adafruit.com/datasheets/MCP9808.pdf

## Pi Command Line

```
i2cdetect -y 1
i2cget -y 1 0x18 5 w
```
