#!/usr/bin/python
import os
os.system("killall -9 XstreamServer.py")
os.system("echo "" > /var/www/errorData/errorMessage.html")

print "Content-type: text/html\n\r\n\r"
print ""