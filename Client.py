# Client.py                                                                                      

# check for overwrite

import ubinascii
import esp
import esp32
import machine
import gc
import socket
import sys
import os
import uos
import time
#from machine import Pin, I2C

#gc.enable()
#gc.collect()

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 8000
EOF = "!`~`|`~!"
Dirs = []
OK = " "
Path = "C:/ESP/"
Q = 0x61
L = []
FullInput = ""
Command = ""

FileName = ""                      # 1st FileName
FileName2 = ""                     # 2nd FileName
Nos = 0                            # Number of Command parameters
DeviceID = ""

# these are the Commands where the FileNeme needs
# to be checked if exists
Menu = {"type": 2,   #   * Check if file exists on Client     
        "rename": 3, #   * Check if file exists on Client
        "delete":2,  #   * Check if file exists on Client
        "rmdir":2,   #   * Check if file exists on Client
        "get":2,     #   * Check if file exists on Client
        "run":2,     #   * Check if file exists on Client       
        "quit":1,}   #
#---------------------------------------------------
def df():
  s = os.statvfs("//")
  return ("{0} MB".format((s[0]*s[3])/1048576))
#---------------------------------------------------
def TimConv(y): # Convert time.localtime() to dd/mm/yy hh:mm:ss
    x = time.localtime(y)
    z = x[2], x[1], x[0], x[3], x[4], x[5]
    return("%2d/%02d/%04d %02d:%02d:%02d " % z[:6])
#---------------------------------------------------
def Send(para):
    global Client
    
    Client.sendall((para).encode())
    return Client.recv(1024).decode()
#-----------------------------------------
def Recv():
    global Client
    
    line = Client.recv(1024).decode()
    Client.sendall((OK).encode())
    return line
#---------------------------------------------------
def get(): # read and send file
    global FileName
        
    for line in open(FileName, "r"):
        Send(line)
    Send(EOF)    
#------------------------------------------------------
def put(): 
    global FileName
    
    f = open(FileName, "w")
    line = ""
    while line != EOF:
        line = Recv()
        if line != EOF:
            f.write(line)
    f.close()
#------------------------------------------------------    
def type(): # read and send file
    global FileName
        
    for line in open(FileName):
        Send(line)
    Send(EOF)        
#----------------------------------------------------------------------------            
def backup():
    global FileName
    
    for fil in os.listdir():
        Send(fil) # send FileName to Server
        FileName = fil
        get()
            
    Send(EOF + EOF)   # after last file
#------------------------------------------------------
def ls():                                                      
    for x in uos.ilistdir():
        y = uos.stat(x[0])
        if y[0] == 32768:
            #           filename        size            datetime         DateTime as string
            Send(x[0] + "|" + str(y[6]) + "|" + str(y[9]) + "|" + TimConv(y[9]))
    Send(EOF)    
#----------------------------------------------
def info():
    uname = os.uname()
    mem_total = gc.mem_alloc()+gc.mem_free()
    free_percent = str((gc.mem_free())/mem_total*100.0)+"%"
    alloc_percent = str((gc.mem_alloc())/mem_total*100.0)+"%"
    MAC = ubinascii.hexlify(network.WLAN().config("mac"),":").decode()
    free = df()
    
    Send("Unique ID .....: {}".format(machine.unique_id()))
    Send("MAC address ...: {}".format(MAC))
    Send("Platform ......: {}".format(sys.platform))
    Send("Version .......: {}".format(sys.version))
    Send("Flash Size ....: {} MBytes".format(esp.flash_size()/(1024*1024)))
    Send("Free Flash ....: {}".format(free))
    Send("Memory")
    Send("   total ......: {} Bytes or {} MBytes".format(mem_total, mem_total/(1024*1024)))
    Send("   usage ......: {} Bytes or {}".format( gc.mem_alloc(), alloc_percent))
    Send("   free .......: {} Bytes or {}".format( gc.mem_free(), free_percent))
    Send("system name ...: {}".format(uname.sysname))
    Send("node name .....: {}".format(uname.nodename))
    Send("release .......: {}".format(uname.release))
    Send("version .......: {}".format(uname.version))
    Send("machine .......: {}".format(uname.machine))
    Send("Frequency .....: {} MHz".format(machine.freq()/1000000.0))
    Send("Temperature ...: {}F".format(esp32.raw_temperature()))
    Send("Hall sensor....: {}".format(esp32.hall_sensor()))
    
    Send(EOF)    
#----------------------------------------------    
def help():
    pass
#----------------------------------------------    
def run():
    global FileName
    
    with open(FileName,"r") as FileName:
        exec(FileName.read())
       
#----------------------------------------------        
def reset():
    global Client
    
    Client.close()
    time.sleep(5)
    machine.reset()    
#----------------------------------------------
def mkdir():
    global FileName
    
    os.mkdir(FileName)
#----------------------------------------------
def delete():
    global FileName
    
    os.remove(FileName)
#----------------------------------------------
def rmdir():
    global FileName
    
    os.rmdir(FileName)    
#----------------------------------------------
def rename():
    global FileName
    
    os.rename(FileName, FileName2)
#----------------------------------------------
def timex():
    x = time.localtime()
    z = x[2], x[1], x[0], x[3], x[4], x[5]
    Send("%2d/%02d/%04d %02d:%02d:%02d " % z[:6])    
#----------------------------------------------
def sleep():
    time.sleep(5)  #delay of 5 seconds
    machine.deepsleep(int(FileName)) 
#----------------------------------------------  
def quit():
    global Client
     
    print("Finished")
    Client.close()
    sys.exit()
#----------------------------------------------
def help():
    pass
#----------------------------------------------      
def OpenClient(): #open Client socket
    global Client
    global port
    global L
   
    try:
        Client.connect((L[2], port))
    except:
        print("Server has not started !!!")
        sys.exit()    
#------------------------------------------------------
def Init():
    global Client
    global L
    
    print("Running Client")
    with open("Conf") as f:
        arg = f.readline()
    L = arg.split("~`")
    
    DeviceID = L[3]
    DeviceID = DeviceID[:-1]
    print("DeviceID = ",DeviceID)
    
    #Files = os.listdir()              # holds all filenames only
    
    OpenClient()             #open socket
    Send(str(DeviceID))      # Send DeviceID  to Server
    L = os.listdir()         
    Send("|".join(L))        # Send list of files to Server
#------------------------------------------------------
def GetPara():
    global Command
    global FileName
    global FileName2
    global Nos
    global Client
    
    FullInput = Recv()
    print()
    print("Recv *" + FullInput + "*")
    print("=========")    
    
    temp = FullInput.split(OK)
    #while "" in temp:
        #temp.remove("")
    Nos = len(temp)
    if Nos > 0:
        Command = temp[0]
    if Nos == 2:
        FileName = temp[1]
    if Nos == 3:
        FileName = temp[1]
        FileName2 = temp[2]
#----------------------- Main Line --------------------
Init()

while True:
    GetPara()
    locals()[Command]() # Call function named Command
    
