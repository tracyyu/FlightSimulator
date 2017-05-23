#!/usr/bin/python
import os
os.system("nohup /var/www/serverApp/demo.py 0<&- &>/dev/null &")

print "Content-type: text/html\n\r\n\r"
print ""
print 'Demo Started!'