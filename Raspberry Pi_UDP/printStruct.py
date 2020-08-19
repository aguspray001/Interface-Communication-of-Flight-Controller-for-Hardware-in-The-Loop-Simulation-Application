import struct
import time
import serial

ser = serial.Serial('/dev/serial0',
                     57600,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout=1)

while True:
	x = struct.pack('i2f', 12, 3.254, 7.123)
	print(x)
	#ser.write(x)
	#print(struct.unpack('i2f', ser.readline()))