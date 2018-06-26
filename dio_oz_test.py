# Creator: Oliver Zhang
# Python classes imported for the program
import time
import io
import serial
import sys
import usb.core
import serial.tools.list_ports as ports

# Decimal VendorID=1667 & ProductID=4369
# Hexadecimal VendorID=0x683 & ProductID=0x1111

# find USB devices
device = usb.core.find(find_all=True)
# loop through devices and check the hexadecimal form of each one's product id
for cfg in device:
  regPID = hex(cfg.idProduct)

  # find a match with the target product id
  if regPID == '0x1111':
    print("file found\n")
    uid = cfg.idProduct

    # search through COM Ports and find location of connected product
    p_list = ports.comports()

    for com in p_list:
      #ser1 = serial.Serial('COM9', 38400, timeout=100)
      if com.pid == uid:
        serID = str(com.device)
        print(serID)

        # record port number and assign product to it
        ser1 = serial.Serial(serID, 38400, timeout=100)

        break
    break

# configure and send commands to the product
i = 0
ser1.write(b"endo 1\r")
while True:
   ser1.write(b"dout 0\r")
   time.sleep(.1)
   ser1.write(b"dout 1\r")
   time.sleep(.1)
   print(i)
   i=i+1
   if i > 10:
     break