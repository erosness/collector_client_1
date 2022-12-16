print ("pypypypy!XXXX")

import debugpy
import serial

# 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
#debugpy.listen(5678)
#print("Waiting for debugger attach")
#debugpy.wait_for_client()
#debugpy.breakpoint()
#print('break on this line')

ser = serial.Serial('/dev/ttyUSB0',920000)
s = ser.read(100)


for loopcnt in range(29):
    line = ser.readline()        
    print(line)



print ("end")


