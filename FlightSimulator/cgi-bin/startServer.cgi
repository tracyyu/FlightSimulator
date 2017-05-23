#!/usr/bin/python
import os

#os.system("nohup /var/www/serverApp/XstreamServer.py 0<&- &>/dev/null &")
#os.system(" at now <<< '/var/www/serverApp/XstreamServer.py' ")

os.system("nohup /var/www/serverApp/XstreamServer.py 0<&- &>/dev/null &")

print "Content-type: text/html\n\r\n\r"
print ""

