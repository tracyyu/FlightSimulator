#!/usr/bin/python

# =========================================================================*
# Copyright (C) Teledyne Technologies, 2013.  All rights reserved.          *
#                                                                           *
#  THIS  IS  CONFIDENTIAL  AND  PROPRIETARY  INFORMATION  OF                *
# TELEDYNE  CONTROLS AND  MAY NOT BE USED OR DISCLOSED BY THE               *
# RECIPIENT  WITHOUT  THE  PRIOR WRITTEN CONSENT  OF TELEDYNE               *
# CONTROLS  AND THEN ONLY IN ACCORDANCE WITH SPECIFIC WRITTEN               *
# INSTRUCTIONS  OF  TELEDYNE CONTROLS.  BY RECEIPT HEREOF, IN               *
# ADDITION  TO ANY  OBLIGATION  THE RECIPIENT  HAS  UNDER ANY               *
# CONFIDENTIALITY  AGREEMENT,   CONTRACT,   OR  LICENSE  WITH               *
# TELEDYNE  CONTROLS,   NEITHER  RECIPIENT  NOR  ITS  AGENTS,               *
# REPRESENTATIVES  OR  EMPLOYEES  WILL  COPY,   REPRODUCE  OR               *
# DISTRIBUTE  THIS INFORMATION,  IN WHOLE OR IN PART,  AT ANY               *
# TIME,   WITHOUT  THE  PRIOR  WRITTEN  CONSENT  OF  TELEDYNE               *
# CONTROLS AND THAT IT WILL KEEP CONFIDENTIAL ALL INFORMATION               *
# CONTAINED HEREIN.                                                         *
# ==========================================================================*
# ***************************************************************************
# Module Name: nLogger.py
#
# Functional Description:
#
# Python script which configures the DHCP server using configuration
# values from switch config and config manager 
#
# Version History:
#
# Version  Date        Author      SPR/SCR  Description
# -------  ----------  ----------  -------  --------------------------------
# E4       09/23/2013  Armen B.    NA       Class used for logging to the 
#											syslog.
#
#
#
#***************************************************************************/

import sys
import syslog 


class nLogger:

	counter = 0
	max_log_output = 3

	WARN = 0
	INFO = 1
	ERR = 2

	def __init__(self, appname, max_log_output = None):
		if appname == None:
			return;

		if max_log_output != None:
			self.max_log_output = max_log_output

		syslog.openlog(appname,syslog.LOG_PID)


	def log(self,loglevel, msg):

		# if we reached maximum number of logging 
		# ignore call and return
		self.counter += 1
		if self.counter >= self.max_log_output:
			return

		if loglevel == self.WARN:
			syslog.syslog(syslog.LOG_WARNING, msg)

		elif loglevel == self.INFO:
			syslog.syslog(syslog.LOG_INFO, msg)

		elif loglevel == self.ERR:
			syslog.syslog(syslog.LOG_ERR, msg)


	def clearLogCount(self):
		self.counter = 0


# application main
if __name__ == '__main__':
	
	def main(argv):

		nlogger_ = nLogger('LogClient.py')

		nlogger_.log(nLogger.WARN, "TEST LOG: *** log as warning ***")
		nlogger_.log(nLogger.INFO, "TEST LOG: *** log as info ***")
		nlogger_.log(nLogger.ERR, "TEST LOG: *** log as error ***")


	main(sys.argv[1:])
