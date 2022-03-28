# Server.py 

# loadup (copy latest version to device, renaming without () 
# fix overwriting
# implement directories
# implement "Are you sure ?
# update RTC timer
# overwrite or not
# wildcards
# include setup ???
# editor
# MQTT
# send info to mobile or laptop

import socket
import sys
import time
from time import strftime
import os
from os import path
import pathlib

s = socket

port = 8000 
Path = 'C:/ESP/'
OK = ' '
EOF = "!`~`|`~!"
cnt = 0
FullInput = ''
temp = ''
Command = ''                       # Command
FileName = ''                      # 1st FileName
FileName2 = ''                     # 2nd FileName
Nos = 0                            # Number of Command parameters
DeviceID = ''
CurrDir = ''
Files = ""
# Function name,   No of Parameters
Menu = { # Valid Commands and no of parameters
        'ls': 1,          
        'help':1,    
        'quit':1,
        'backup':1,
        'reset':1,  
        'restore':1,   # NOT DONE YET
        'info':1,
        'timex':1,
        'exec':1,
        'type': 2,   
        'delete':2,  
        'mkdir':2,   
        'rmdir':2,   
        'get':2,     
        'put':2,     
        'run':2,
        'freq':2,
        'sleep':2,    
        'rename': 3 
        }   


Check = { # Commands where file existence on Server need checking
        'type': 2,     # if exists on Device
        'delete':2,    # if exists on Device
        'rmdir':2,     # if exists on Device
        'run':2,       # if exists on Device
        'get':2,       # if exists on Device
        'put':2,       # if NOT exists on Server
        'mkdir':2,     # if NOT exists on Device
        'rename': 3,   # if FileName exists on Device and
                       # FileName2 NOT exist on Device
        }     
        
s = socket
 
#-----------------------------------------
def Send(para):
    global Server
    
    Server.sendall((para).encode())
    return Server.recv(1024).decode()
#-----------------------------------------
def Recv():
    global Server
    
    line = Server.recv(1024).decode()
    Server.sendall((OK).encode())
    return line
#-----------------------------------------
def NextFile(x):
    global cnt
    global CurrDir
    
    os.chdir(CurrDir)
    cnt = cnt + 1    
    nam, ext = os.path.splitext(x)
    
    if (nam + '3' + ext) in os.listdir():
        os.remove((nam + '3' + ext))
        os.rename((nam + '2' + ext), (nam + '3' + ext))
        os.rename((nam + '1' + ext), (nam + '2' + ext))
        os.rename((nam + ''  + ext), (nam + '1' + ext))   
        return (nam + ext)
    else:
         if (nam + '2' + ext) in os.listdir():
             os.rename((nam + '2' + ext), (nam + '3' + ext))
             os.rename((nam + '1' + ext), (nam + '2' + ext))
             os.rename((nam + ext), (nam + '1' + ext))
             return (nam + ext)
         else:
             if (nam + '1' + ext) in os.listdir():
                  os.rename((nam + '1' + ext), (nam + '2' + ext))
                  os.rename((nam + ext), (nam + '1' + ext))
                  return (nam + ext)
             else:
                 if (nam + ext) in os.listdir():
                     os.rename((nam + ext), (nam + '1' + ext))
                     return (nam + ext)
                 else:
                     return (nam + ext)

#-----------------------------------------
def help(): #OK print Help
    print(53*'-')
    print('COMMAND [PARAMETER1] [PARAMETER2]')
    print(53*'-')
    print('delete filename             - Delete file from Device')
    print('rename filename1 filename2    - Rename file on Device')
    print('type filename                - Print file from Device')
    print('mkdir directory          - Create directory on Device')          
    print('rmdir directory          - Delete directory on Device')              
    print('get filename              - Download file from Device')                
    print('put filename                  - Upload file to Device') 
    print('run filename                    - Runs file on Device') 
    print('backup         Download all changed files from Device') 
    print('ls                             - List files on Device') 
    print('timex                     Print Local and Device time')
    print('reset           Reset Device, runs boot, main, Client')
    print('sleep            - Puts device to Deep sleep for n ms')
    print('help                               - Prints this help') 
    print('quit                          - Terminate this script') 
    print(53*'-')
    print()
#-----------------------------------------
def OpenServer(): # Open Server socket
    global Server
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind( ('192.168.1.117', port) )
    s.listen(1) 
    print('Waiting on Port',port)
    Server, address = s.accept()
    print("Connected to: " + str(address))
    print()
#----------------------------------------------
def hx(a):
    s = ''
    for i in range(len(a)):
        s = s + hex(ord(a[i]))
    return s
#----------------------------------------------    
def get(): #OK Copy file from Device
    global FileName
    global CurrDir
   
    print('   Copying ' + FileName)
    F = open(CurrDir + NextFile(FileName), 'w')
    line = ''
    while line != EOF:
        line = Recv()
        line = line.replace('\r','')
        #print(len(line))
        #print(hx(line))
        if line != EOF:
             F.write(line)
             print('.', end="")
    F.close()
    print()
#---------------------------------------------- 
def put(): # OK # copy file to Device 
    global CurrDir
    global Files
    
    print('   Copying ' + FileName)
    with open(CurrDir + FileName, 'r') as f:
        for line in f:
            Send(line)
            print('.', end="")
    Send(EOF)
    print()
    Files.append(FileName)
#-------------------------------------------------------
def type(): #OK Type file from Device
    print(50*'-')
        
    line = ''
    while line != EOF:
        line = Recv()
        if line != EOF:
            print(line, end="")
    print()

    print(50*'-')
    print()
#-----------------------------------------------
def info():
    print(50*'-')
        
    line = ''
    while line != EOF:
        line = Recv()
        if line != EOF:
            print(line)
    #print()

    print(50*'-')
    print()
#------------------------------------------------------    
def backup(): # copy aCommand modified file from Device
    global FileName
    
    print(50*'-')
    while True:
        FileName = Recv()         # get filename from Client
        if FileName == EOF + EOF: # after last file received
            break 
        else:
            get()
    print(50*'-')
#---------------------------------------------------    
def ls(): # list files on Device
    global DeviceID
    
    Tot = 0
    print('FileName (DeviceID=' + DeviceID + ')     Size       Date      Time')
    print(53*'-')
    
    while True:
        line = Recv()
        if line != EOF:
            if len(line) > 3:
                L = line.split('|')
                Tot = Tot + int(L[1])
                x = int(L[1])
                print(L[0].ljust(20) +  f"{x:,}".rjust(10) + '    ' + L[3])
        else:
            break
        
    print(53*'-')
    print('Total Size'.ljust(24) + f"{Tot:,}")  
    print()
#-------------------------------------------------
def quit(): #OK quit this program
    global Server
    
    Send('quit')
    print()
    print('Server Finished')
#     Server.close()
    Server.shutdown(1)
    Server.close()
    sys.exit()
#-------------------------------------------------
def run(): #OK run a file on the device
    pass
#-------------------------------------------------
def mkdir(): #OK create a directory on the Device
    pass
#-----------------------------------------------
def delete(): #OK delete a file on the Device
    global Files
    global FileName
    
    Files.remove( FileName)
#-------------------------------------------------
def rmdir(): #OK delete a directory on the Device
    global Files
    global FileName
    
    Files.remove(FileName)
    pass
#-------------------------------------------------
def rename(): #OK rename a file on the Device
    global FileName
    global FileName2
    
    Files.remove(FileName)
    Files.append(FileName2)
#-----------------------------------------------
def timex():
    tim = Recv()
    print('Device time:', tim)
    x = time.localtime()
    z = x[2], x[1], x[0], x[3], x[4], x[5]
    print("Local time:  %2d/%02d/%04d %02d:%02d:%02d " % z[:6])
#-------------------------------------------------
def sleep():
    pass
#-------------------------------------------------
def freq():
    print('sdas')
    pass
#-------------------------------------------------
def reset(): #OK reset Device
    global Server
    
    Server.close()
    Init()
#------------------------------------------------------------
def OpenServer(): # Open Server socket
    global Server

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind( ('', port) )
    s.listen(5)
    print('Waiting on Port',port)
    Server, address = s.accept()
    print("Connected to: " + str(address))
#------------------------------------------------------    
def Init():
    global DeviceID
    global CurrDir
    global Files
    if not os.path.isdir(Path):
        os.mkdir(Path)     
     
    OpenServer()
    
    DeviceID = Recv()    # Get DeviceID from Client
    Fil = Recv()       # Get list of all files from Client
    Files = Fil.split("|")
   
    CurrDir = Path + DeviceID + '/'
    print('DeviceID =',DeviceID)
    print()
    try:                             # check if Device directory exists
        mkdir(MyPath + DeviceID)     # if not create it
    except:
        pass
#---------------------------------------------------------    
def GetPara():
    global Command 
    global FileName
    global FileName2
    global Nos
    global FullInput
    global Files
    
    Command = ''
    FileName = ''
    FileName2 = ''
    Nos = 0
    
    FullInput = input('Input: ')
    temp = FullInput
    if temp != '':                              
        temp = FullInput.split(OK)
        while "" in temp:
            temp.remove("")
        Nos = len(temp)
        if Nos > 0:
            Command = temp[0]
        if Nos == 2:
            FileName = temp[1]
        if Nos == 3:
            FileName = temp[1]
            FileName2 = temp[2]
    else:
        print('   Invalid Command')
        return False

    #print('=' + str(Nos) + '=' + Command + '=' + FileName + '=' + FileName2 + '=')
    
    if Command == 'quit':
        quit()
        
    if Command not in Menu:          # check for valid Command
        print('   Invalid Command')
        return False 
            
    if Nos != Menu[Command]:         # check for valid number of parameters
        print('   Invalid no of parameters')
        return False
    
    if Menu[Command] == 1:           # no FileName so OK
        return True
    
    if Command not in Check:         # check files on device
        return True 
    else:
        if (Command == 'type') or (Command == 'delete') or (Command == 'rmdir') or (Command == 'run') or (Command == 'get'):
            if FileName not in Files:
                print('   ' + FileName + " not on Device")
                return False 
            else:
                return True
   
    if Command == 'put':
        if os.path.exists(CurrDir + FileName):
            pass
        else:
            print('   ' + FileName + " not on Server")
            return False
        
        if FileName in Files:
            print('   ' + FileName2 +' is already on Device')
            inp = input('   Overwrite (y/n)')
            if inp == 'y':
                return True
            else:
                print('   ' + FileName + ' not Copied')
                return False
        else:
            return True
        
    if Command == 'rename':
        if FileName not in Files:
            print('   ' + FileName + ' not on device')
            return False
        if FileName2 in Files:
            print('   ' + FileName2 +' is already on Device')
            inp = input('   Overwrite (y/n)')
            if inp == 'y':
                return True
            else:
                print('   ' + FileName + ' not renamed')
            return False
        else:
            return True
#--------------------- Main line --------------------        
Init()

while True:
    if GetPara():
        Send(FullInput)
        locals()[Command]()
        print()
    else:
        print()
 