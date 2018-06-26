# Creator: Oliver Zhang
import time
import io
import serial
import sys
import usb.core
import serial.tools.list_ports as ports

def findProdPort():
    # find USB devices
    device = usb.core.find(find_all=True)
    # loop through devices and check the hexadecimal form of each one's product id
    for cfg in device:
        regPID = hex(cfg.idProduct)

        # find a match with the target product id
        if regPID == '0x1111':
            uid = cfg.idProduct

            # search through COM Ports and find location of connected product
            p_list = ports.comports()

            for com in p_list:
                #ser1 = serial.Serial('COM9', 38400, timeout=100)
                if com.pid == uid:
                    serID = str(com.device)
                    return serID

ser1 = serial.Serial(findProdPort(), 38400, timeout=100)

i = 0
while True:
   ser1.write(b"led 1\r")
   time.sleep(1)
   ser1.write(b"led 2\r")
   time.sleep(1)
   ser1.write(b"led 4\r")
   time.sleep(1)
   ser1.write(b"led 7\r")
   time.sleep(1)
   print(i)
   i=i+1
   if i > 3:
    ser1.write(b"led 6\r")
    break