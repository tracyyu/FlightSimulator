#!/bin/bash

ps -ef | grep -i xstream | grep -v grep
if [ $?  -eq "0" ]; then MESSAGE="Server Running"; else MESSAGE="Server Not Running"; fi

echo "Content-type: text/html"
echo ""
echo "<html> <body>"
echo $MESSAGE
echo "</body></html>"