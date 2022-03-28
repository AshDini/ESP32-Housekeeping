# boot.py                                                     

import network

#------------------------------------------------------    
with open("Conf") as f:
    arg = f.readline()
L = arg.split("~`")
#------------------------------------
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print("Connecting to network")
    sta_if.active(True)
    sta_if.connect(L[0], L[1])
    while not sta_if.isconnected():
        pass
print("network config:", sta_if.ifconfig())
#------------------------------------------------------    

 