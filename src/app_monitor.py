"""
  - Add this line to /etc/rc.local (before the exit 0):
  -   /home/pi/ONBOOT.sh 2> /home/pi/ONBOOT.errors > /home/pi/ONBOOT.stdout &
  - Add the following ONBOOT.sh script to /home/pi and make it executable:
  
#!/bin/bash
cd /home/pi/home-freezerMonitor
python3 app_monitor.py  
"""

import hardware
import datetime
import json
import aiohttp.web  # python3 -m pip install aiohttp


async def root_handler(request):

    data = {
        'value' : HARDWARE.read_temperature(),
        'time' : str(datetime.datetime.now())
        }

    return aiohttp.web.Response(text=json.dumps(data), content_type='application/json')


HARDWARE = hardware.Hardware()

app = aiohttp.web.Application()
app.router.add_route('*', '/', root_handler)
app.router.add_route('*', '/data/freezer', root_handler)

if __name__ == '__main__':
    aiohttp.web.run_app(app, port=80)