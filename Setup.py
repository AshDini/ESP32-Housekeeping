# Setup.py

import serial
import time
import socket
import sys
import os

Var = ''
Sep = '~`'

Var = ''
HostName = ''
HostPass = ''
HostIP = ''
DeviceID = ''
MainDirectory = ''

def Send(s):
    global ser
    print('.', end="")
    #print(s)
    ser.write((s +'\r\n').encode())
    time.sleep(.3)
    z = ser.read(ser.in_waiting)
#------------------------------------------------------------- 
def CopyBoot():
    Send("f = open('boot.py','w')")
    with open('boot.py') as ff:
        for line in ff:
            StringToSend = """f.write('""" + line + """\\n')"""    
            Send(StringToSend)
    Send("f.close()")
#-------------------------------------------------------------
def CopyClient():
    Send("f = open('Client.py','w')")
    with open('Client.py') as ff:
        for line in ff:
            StringToSend = """f.write('""" + line + """\\n')"""    
            Send(StringToSend)
    Send("f.close()")
#-------------------------------------------------------------      
def GetDeviceID():
    global DeviceID
    
    while True:
        DeviceID = input('DeviceID: ')
        if len(DeviceID) != 2:
            print('DeviceID must be 2 digits')
        else:
            if DeviceID in os.listdir(MainDirectory):
                ans = input('Device Directory already exists, continue (y/n)')
                if ans != 'y':
                    sys.exit()
            return DeviceID
#-------------------------------------------------------------    
def GetParams():
    global HostName
    global HostPass
    global HostIP
    
    HostName = input('Host Name: ')
    Var = HostName + Sep

    HostPass = input('Host Password: ')
    Var = Var + HostPass + Sep
    
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    st.connect(('10.255.255.255', 1))  # get Host IP
    HostIP = st.getsockname()[0]
    st.close()
    
    Var = Var + HostIP + Sep + MainDirectory + '/'
   
    f = open('BaseConf','w')
    f.write(Var)
    f.close()
#-------------------------------------------------------------    
def OpenSerial():
    global ser
    
    bps = 115200
    timex = 5
    for i in range(10):
        portx = 'COM' + str(i)
        try:
            ser = serial.Serial(portx,bps,timeout=timex)
            print('COM' + str(i) + ' is available')
            ser.close()
        except:
            pass

    print()
    portx = input('COMPort: ')
    portx = portx.upper()
    print(portx)
    try:
        bps = 115200
        timex = 5
        ser = serial.Serial(portx,bps,timeout=timex)
    except:
        print('invalid COMPort')
        sys.exit()
#-------------------------------------------------------------
MainDirectory = os.getcwd()
print('the scripts will be installed in ', MainDirectory)
ans = input('Is that OK (y/n): ')
if ans != 'y':
    sys.exit()
    
if 'BaseConf' not in os.listdir(MainDirectory):
    GetParams()

OpenSerial()     
GetDeviceID()

Var = HostName + Sep + HostPass + Sep + HostIP + Sep + DeviceID
StringToSend = """f.write('""" + Var + """\\n')"""
Send("f = open('Conf','w')")         # write Conf to Device
Send(StringToSend)
Send("f.close()")
time.sleep(1)

Var = "import Client"
StringToSend = """f.write('""" + Var + """\\n')"""
Send("f = open('main.py','w')")         # write Conf to Device
Send(StringToSend)
Send("f.close()")
    
CopyBoot()
CopyClient()

ser.close()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             