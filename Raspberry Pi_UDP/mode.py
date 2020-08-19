import serial
import time
import sys
import select
import struct
from multiprocessing import Process

# Serial Configuration
ser = serial.Serial('/dev/serial0',
                     38400,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout=1)

def mode_1():
	print("Mode Auto")
	ser.write(chr(97))

def mode_2():
	print("Mode Stabilize")
	ser.write(chr(115))

def mode_3():
	print("Mode Loiter")
	ser.write(chr(108))

def mode_4():
	print("Mode FBWA")	
	ser.write(chr(102))

def mode():
	while True:
		input = select.select([sys.stdin], [], [], 1)[0]
		if input:
			key = sys.stdin.readline().strip()
			if(key == "1"):
				mode_1()
			elif(key == "2"):
				mode_2()
			elif(key == "3"):
				mode_3()
			elif(key == "4"):
				mode_4()
			else:
				break

def read_serial():
	while True:
		data = ser.readline()
		print(data)
		#print(len(data))

if __name__ == "__main__":
	Process(target=read_serial).start()

mode()
