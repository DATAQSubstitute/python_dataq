# Creator: Oliver Zhang
# Python classes imported for the program
import time
import io
import serial
import sys
import usb.core
import serial.tools.list_ports as ports
import psutil
import os
import keyboard

# Decimal VendorID=1667 & ProductID=4369
# Hexadecimal VendorID=0x683 & ProductID=0x1111

# find USB devices
device = usb.core.find(find_all=True)
# loop through devices and check the hexadecimal form of each one's product id
for cfg in device:
  regPID = hex(cfg.idProduct)

  # find a match with the target product id
  if regPID == '0x2107':
    print("Device found\n")
    uid = cfg.idProduct

    # search through COM Ports and find location of connected product
    p_list = ports.comports()

    for com in p_list:
      #ser1 = serial.Serial('COM9', 38400, timeout=100)
      if com.pid == uid:
        serID = str(com.device)

        # record port number and assign product to it
        ser1 = serial.Serial(serID, 38400, timeout=0)

        break
    break
i = 0


ser1.write(b"ps 6\r")
print(ser1.readline())

ser1.write(b"dec 15\r")
print(ser1.readline())

ser1.write(b"srate 3000\r") #   20000 samples / sec
print(ser1.readline())

ser1.write(b"slist 0 0\r")
print(ser1.readline())

ser1.write(b"slist 1 1\r")
print(ser1.readline())

ser1.write(b"slist 2 2\r")
print(ser1.readline())

ser1.write(b"slist 3 3\r")
print(ser1.readline())

ser1.write(b"slist 4 4\r")
print(ser1.readline())

ser1.write(b"slist 5 5\r")
print(ser1.readline())

ser1.write(b"slist 6 6\r")
print(ser1.readline())

ser1.write(b"slist 7 7\r")
print(ser1.readline())

ser1.write(b"start\r")

j = 0
i = 0
k = 0
m_bytes = []
#m_bytes.append(1)
with open("recdaq.bin", "wb") as fh:
# configure and send commands to the product
  while True:

    i = ser1.inWaiting()
    if i > 256:
      #print('.', end='', flush=True)
      #com = ser1.read()
      #m_bytes[k] = com
      #m_bytes=ser1.read()
      #k=k+1
      fh.write(ser1.read(256))
      j=j+1
    if keyboard.is_pressed('s'):    #if key 's' is pressed 
      keyboard.release('s')
      ser1.write(b"stop\r")
      fh.close()
      break
