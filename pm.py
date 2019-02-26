import RPi.GPIO as GPIO
import serial
import Adafruit_DHT
import time
import sys
import datetime
from struct import *
from time import gmtime, strftime
debug=1


actual_time = strftime("%Y-%m-%d %H-%M-%S", gmtime())


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()



# Remove the space, ottowei, 2019022601
file = open("PMdata-" + str(actual_time) + ".txt", "w")

while True:

    print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    humidity, temperature = Adafruit_DHT.read_retry(11 ,18) 
    # Add Temp print, ottowei, 2019022601
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    
    
    class g3sensor():
        def __init__(self):
            if debug: print "init"
            self.endian = sys.byteorder
    
        def conn_serial_port(self, device):
            if debug: print device
            self.serial = serial.Serial(device, baudrate=9600)
            if debug: print "conn ok"

        def check_keyword(self):
            if debug: print "check_keyword"
            while True:
                token = self.serial.read()
                token_hex=token.encode('hex')
                if debug: print token_hex
                if token_hex == '42':
                    if debug: print "get 42"
                    token2 = self.serial.read()
                    token2_hex=token2.encode('hex')
                    if debug: print token2_hex
                    if token2_hex == '4d':
                        if debug: print "get 4d"
                        return True
                    elif token2_hex == '00': # fixme
                        if debug: print "get 00"
                        token3 = self.serial.read()
                        token3_hex=token3.encode('hex')
                        if token3_hex == '4d':
                            #if debug: print "get 4d"
                            return True
		    
        def vertify_data(self, data):
            if debug: print data
            n = 2
            sum = int('42',16)+int('4d',16)
            for i in range(0, len(data)-4, n):
                print data[i:i+n]
                sum=sum+int(data[i:i+n],16)
            versum = int(data[40]+data[41]+data[42]+data[43],16)
            if debug: print sum
            if debug: print versum
            if sum == versum:
                print
	
        def read_data(self):
            data = self.serial.read(22)
            data_hex=data.encode('hex')
            if debug: self.vertify_data(data_hex)
            pm1_cf=int(data_hex[4]+data_hex[5]+data_hex[6]+data_hex[7],16)
            pm25_cf=int(data_hex[8]+data_hex[9]+data_hex[10]+data_hex[11],16)
            pm10_cf=int(data_hex[12]+data_hex[13]+data_hex[14]+data_hex[15],16)
            pm1=int(data_hex[16]+data_hex[17]+data_hex[18]+data_hex[19],16)
            pm25=int(data_hex[20]+data_hex[21]+data_hex[22]+data_hex[23],16)
            pm10=int(data_hex[24]+data_hex[25]+data_hex[26]+data_hex[27],16)
            if debug: print "pm1_cf: "+str(pm1_cf)
            if debug: print "pm25_cf: "+str(pm25_cf)
            if debug: print "pm10_cf: "+str(pm10_cf)
            if debug: print "pm1: "+str(pm1)
            if debug: print "pm25: "+str(pm25)
            if debug: print "pm10: "+str(pm10)
            data = [pm1_cf, pm10_cf, pm25_cf, pm1, pm10, pm25]

            #mylcd.lcd_display_string("T={0:0.1f}C H={1:0.1f}%%".format(temperature, humidity), 1) 
            #mylcd.lcd_display_string("PM1: %s" % pm1, 2)
            #mylcd.lcd_display_string("PM2.5: %s " % pm25, 3)
            #mylcd.lcd_display_string("PM10: %s "  % pm10, 4)
            
            file.write('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            file.write("  Humidity: %s" % humidity)
            file.write("  Temperature in C: %s" % temperature)
            file.write("    PM 1: %s" % pm1)
            file.write("    PM 2.5: %s" % pm25_cf)
            file.write("    PM 10: %s" % pm10_cf)
            file.write("\n")
            file.flush()

            self.serial.close()
	    if debug: print data
            return data


        def read(self, argv):
            tty=argv[0:]
            self.conn_serial_port(tty)
            if self.check_keyword() == True:
                self.data = self.read_data()
                #if debug: print self.data
                return self.data

    if __name__ == '__main__': 
	
        air=g3sensor()
        while True:
            pmdata=0
            try:
                pmdata=air.read("/dev/ttyUSB0")
            except: 
                next
            if pmdata != 0:
                #print pmdata
                break

	    time.sleep(30)
	
