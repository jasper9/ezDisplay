# structure from:https://learn.adafruit.com/pyportal-air-quality-display
# text ideas from:  https://learn.adafruit.com/pyportal-bitcoin-value-display/bitcoin-value-display
# library link   https://github.com/adafruit/Adafruit_CircuitPython_PyPortal/blob/master/adafruit_pyportal.py

# tips on json from https://hackaday.io/project/163309-circuitpython-hackaday-portal-pyportal
# ujson renamed to json in 4.x https://github.com/adafruit/circuitpython/releases

import sys
import time
import board
import json
from adafruit_pyportal import PyPortal
import ezDisplay 

cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)
sys.path.append(cwd)

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

##############################################################################

# FILL IN VALUES HERE

DESCRIPTION = "Outside Temperature"
PIN = "V4"
DATA_SOURCE = "http://blynk-cloud.com/"+secrets['blynk_key']+"/get/" + PIN
DATA_LOCATION = [0]
SUFFIX = "°f"
NUM_DECIMALS = 1

# DESCRIPTION = "PVTL Stock Price"
# STOCK = "pvtl"
# FIELD = "latestPrice"
# DATA_SOURCE = "https://cloud.iexapis.com/beta/stock/" + STOCK + "/quote?token="+secrets['iex_key']+""
# DATA_LOCATION = [FIELD]
# SUFFIX = "$"
# NUM_DECIMALS = 2

##############################################################################

pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=DATA_LOCATION,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=0x000000)
gfx = ezDisplay.ezDisplay(pyportal.splash, am_pm=True, celsius=False)
localtile_refresh = None
weather_refresh = None
while True:
    if (not localtile_refresh) or (time.monotonic() - localtile_refresh) > 3600:
        try:
            print("Getting time from internet!")
            pyportal.get_local_time()
            localtile_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 60:
        try:
            value = pyportal.fetch()
            print("Response is", value)
            gfx.display_value(value, DESCRIPTION, SUFFIX, NUM_DECIMALS)
            weather_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue
    gfx.update_time()
    time.sleep(30)
