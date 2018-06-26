# Creator: Oliver Zhang
# Python classes imported for the program
import time
import io
import serial
import sys
import usb
import serial.tools.list_ports as ports
import psutil
import os
#import win32api, win32process, win32con
import keyboard
from usb import core

def txRxPrn(msg): #transmit message, receive response, print response
  ser1.write(msg)
  while True:
    if ser1.inWaiting() > 0:
      print(ser1.readline())
      break

def highpriority():
    """ Set the priority of the process to high."""

    try:
        sys.getwindowsversion()
    except AttributeError:
        isWindows = False
    else:
        isWindows = True

    # pylint: disable=no-member
    #if isWindows:
        # Based on:
        #   "Recipe 496767: Set Process Priority In Windows" on ActiveState
        #   http://code.activestate.com/recipes/496767/
        #   import win32api,win32process,win32con
        #pid = win32api.GetCurrentProcessId()
        #handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        #win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
    #else:
    import os

    os.nice(20)

# Decimal VendorID=1667 & ProductID=4369
# Hexadecimal VendorID=0x683 & ProductID=0x4109

# find USB devices
device = usb.core.find(find_all=True)
# loop through devices and check the hexadecimal form of each one's product id
for cfg in device:
  regPID = hex(cfg.idProduct)
  #print(regPID)

  # find a match with the target product id
  if regPID == '0x4109':
    print("Device found\n")
    uid = cfg.idProduct

    # search through COM Ports and find location of connected product
    p_list = ports.comports()

    for com in p_list:
      if com.pid == uid:
        serID = str(com.device)

        # record port number and assign product to it
        ser1 = serial.Serial(serID, 38400, timeout=0)

        break
    break

highpriority()    #set application to high

j = 0
i = 0
k = 0
m_bytes = []

ser1.write(b"stop\r")
while True:
  i = ser1.inWaiting()
  if i > 0:
    m_bytes = ser1.read()
  else:
    break

txRxPrn(b"ps 3\r")

txRxPrn(b"dec 10\r")

txRxPrn(b"srate 3000\r") #   20000 samples / sec

txRxPrn(b"slist 0 0\r")

txRxPrn(b"slist 1 1\r")

txRxPrn(b"slist 2 2\r")

txRxPrn(b"slist 3 3\r")

txRxPrn(b"slist 4 4\r")

txRxPrn(b"slist 5 5\r")

txRxPrn(b"slist 6 6\r")

txRxPrn(b"slist 7 7\r")


#m_bytes.append(1)
fh = open("recdaq.bin", "wb")
time.sleep(1)
ser1.write(b"start\r")
# configure and send commands to the product
while True:
  i = ser1.inWaiting()
  while i > 512:
    fh.write(ser1.read(512))

    if keyboard.is_pressed(chr(27)):    #if key esc is pressed 
        keyboard.read_key()
        ser1.write(b"stop\r")
        time.sleep(1)
        m_bytes = ser1.read()
        ser1.close()
        fh.close()
        print("All Done!")
        break

