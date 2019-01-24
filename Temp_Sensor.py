# Add for Temperature and Humidity Sensor, ottowei, 20190124

import sys

import Adafruit_DHT

print('Use to show temperature and humidity!')

humidity, temperature = Adafruit_DHT.read_retry(11 ,17) 

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)


