# ESP32-Housekeeping

Nowadays, I work mainly with Microcontrollers (esp32, 8266, NRF8240, etc), using Micropython or CircuitPython, and have a couple of dozen or more, working in various environments.

Most of these Devices are battery powered, and in order to update the various scripts, I would have to remove them from their permanent places in order to plug them into a USB cable which in some cases are almost impossible.

As most of these Devices, perform totally different functions, I also have a considerable problem knowing which scripts (and versions) are on each Device.

So I decided to write a small "Housekeeping System" for these microcontrollers using WIFI, (OTA) and have a central repository of all the scripts for all the Devices. I wrote a 2 digit ID with a felt tip pen on each Device to identify them.

I use a Win10 PC for my development, and use Thonny or Visual Studio to program the Devices. But since the Server (on the Host) is written in Python it would require a very small effort to change it for a different operating system. I also have a version of a (slightly modified) Server which I use on my android tablet using QPython 3L

I am not an experienced Python programmer, so I would like to apologise to the "Pythonic Gods" for my transgressions.

I would also like to thank the many people who helped me on various internet sites, when I ran into difficulties. 

All POLITE suggestions will be welcomed.


SETUP PROCEDURE
---------------
  1) Create a directory of your choice called the MainDirectory
  2) Copy ESP.zip and Readme.txt to the MainDirectory
  3) Extract all files from ESP.zip to the MainDirectory.
  4) Open a terminal in this direcory
  5) Run "python Setup.py"
  6) Run python Server.py It will wait on Port 8000 for the Client to be loaded  					
  7) Hard reset the ESP32. It will run boot.py, main.py, and Client.py
  8) The server is now ready to issue Commands, type "help" to see all available Commands
		
		
Version 0.5
===========
	This version does not check if files are being overwritten, so *BE WARNED*
	This version will only handle files in the root directory of the device being programmed
	
		
More detailed descriptions on each of the available Commands:
-------------------------------------------------------------
	delete filename            - deletes the file from the Device
	rename filename1 filename2 - renames filename1 to filename2 on the Device
	type filename              - prints the contents of the file
	mkdir directory            - creates a directory on the Device
	rmdir directory            - removes a directory from the Device
	get filename               - copies the file from the device into the Device's directory this will keep up to 3 versions.
                                  the most recent is the original filename, ie. "try.py"
                                  the previous version will be "try1.py"
                                  the previous version will be "try2.py"
                                  the oldest version will be "try3.py"
	put filename               - copies the file from the Device's directory to the Device		
	run filename               - runs the script
	backup                     - copies ALL the files from the Device to the Device's directory keeping up to 3 versions of each file.
	ls                         - prints all the files and properties on the Device
	timex                      - displays the current date and time, of the Host and the Device
	reset                      - hard resets the device, which in turn runs: boot.py, main.py and Client.py
	sleep n                    - puts the device into deep sleep for n microseconds
	help                       - displays a short help
	quit                       - terminates both the Server and the Client
		
	
