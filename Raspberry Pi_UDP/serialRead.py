import serial
import time
from struct import *
import struct
from ctypes import *
import socket

ser = serial.Serial('/dev/serial0',
                     38400,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout=1)

while True:
	data = ser.readline()
	print(data)

	# Datalog	
	#datalog = open("/root/data.txt", "a")
	#datalog.write(data)
	#datalog.close()