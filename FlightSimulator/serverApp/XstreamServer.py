#!/usr/bin/python
import globals
import json
import time
import csv
import commands
import sys
import signal
import os

from datetime import datetime
from UDPReceiver import *
from ADBPBinaryProcessor import *
from TableHTMLGenerator import *
from nLogger import *

# GLOBAL VARIABLES
# ----------------
quit = False

# callback when sigterm is called 
def signal_term_handler(signal, frame):
    print("SIGTERM...Exiting")
    quit = True
    exit(0)

def WriteToError(msg):
    try:
        t_errorFile = open(globals.ERROR_FILE_PATH, "w")
        if msg:
            t_errorFile.write(msg)
        t_errorFile.close()
    except IOError as e:
	    nlogger_.log(nLogger.INFO, "I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError:
        nlogger_.log(nLogger.INFO, "Could not convert data to an integer.")
    except:
        nlogger_.log(nLogger.ERR, "Unexpected error: {0}".format(sys.exc_info()[0]))


if __name__ == '__main__':

    try:
        nlogger_ = nLogger('XStreamServer',100)
        nlogger_.log(nLogger.WARN, "Started XStreamServer")

        # catch sigterm signal
        signal.signal(signal.SIGTERM, signal_term_handler)

        globals.init()
        adbpBinProcessor = ADBPPacketProcessor()
        tableHtmlGen = TableHTMLGenerator()

        receivedDataFile = None  # record the flight data in encrypted mode
        csvLogFile = None  # decrypted log file that includes received data
        previousDest = None
        previousOrigin = None
        latlngList = []

        # We use a hacky way to grab IP value
        intf = 'eth0'
        intf_ip = commands.getoutput("ip address show dev " + intf).split()
        intf_ip = intf_ip[intf_ip.index('inet') + 1].split('/')[0]

        localIpAddress = intf_ip
        queue = Queue.Queue()
        receiver = UDPReceiver(queue)
        receiver.SetBroadcastIP(localIpAddress)
        receiver.SetBroadcastPort(globals.PORT_NUMBER)

        if not receiver.StartReceiving():
            nlogger_.log(nLogger.ERR, "error starting adbp receiver")
            exit(1)

        while not quit:

            nlogger_.clearLogCount()

            # get the received udp packet, and wait for some time if the
            # packet doesn't arrive in RECEIVE amount of time then ignore
            try:
                receivedData = queue.get(True, globals.RECEIVE_TIMEOUT_SEC)
                nlogger_.log(nLogger.INFO, "received data")

            except Queue.Empty:
                nlogger_.log(nLogger.INFO,"Queue is empty and timeout has reached")
                t_errorMsg = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S]") + \
                             "  Data not received. Timeout reached seconds: " + \
                             str(globals.RECEIVE_TIMEOUT_SEC)
                WriteToError(t_errorMsg)
                continue
            except KeyboardInterrupt:
                nlogger_.log(nLogger.INFO,"KeyboardInterrupt called queue to return")
                quit = True
                continue
            except:
                nlogger_.log(nLogger.ERR, "Unexpected except")


            nlogger_.log(nLogger.INFO, "Clear error file")

            # clear error string file
            WriteToError(None)
            nlogger_.log(nLogger.INFO, "Started Processing")

            # processes the data and outputs a dictionary
            t_procData = adbpBinProcessor.Process(receivedData)
            nlogger_.log(nLogger.INFO, "Processed Data OK")

            # if adbp processing returned null then break
            if t_procData is None:
                nlogger_.log(nLogger.INFO, "Processed Data is None")
                t_errorMsg = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S]") + \
                             "Data is empty"
                WriteToError(t_errorMsg)
                continue
            

            # add up all the fuel items
            t_totalFuel = t_procData['FQTLOT'] + t_procData['FQTLIT'] + t_procData['FQTCT'] + \
                          t_procData['FQTRIT'] + t_procData['FQTROT'] + t_procData['FQTACT1'] + t_procData['FQTACT2'] + \
                          t_procData['FQTRCT'] + t_procData['FQTTRIMT']


            # create a total fuel item and pass to the html creator
            t_procData['TOTFUEL'] = t_totalFuel


            # if the flight is new then create a new file to hold the received encrupted data
            # and the processed file that holds all
            if t_procData['DESTINATION'] != previousDest and \
                            t_procData['ORIGIN'] != previousOrigin:
                # origin and destination has changed so update those values
                previousOrigin = t_procData['ORIGIN']
                previousDest = t_procData['DESTINATION']

                # create a filename form the flight number - destorigin and timestamp
                t_fileName = t_procData['FLTNUM'].strip() + "_" + t_procData["DESTINATION"].strip() + "_" + \
                             t_procData["ORIGIN"].strip() + "_" + datetime.utcnow().strftime("%Y%m%d")

                # create the file using the filename and give it .bin extension
                receivedDataFile = open(globals.HISTORY_DIR + t_fileName + ".bin", "w")

                # create a csv file to write the log messages
                t_csvLogFile = open(globals.HISTORY_DIR + t_fileName + ".csv", "w")
                csvLogFile = csv.DictWriter(t_csvLogFile, t_procData.keys())
                csvLogFile.writeheader()


            # save the data to a file only if the file is open
            if receivedDataFile is not None:
                receivedDataFile.write(receivedData)

            if csvLogFile is not None:
                csvLogFile.writerow(t_procData)

            # write out the values
            t_latlongObj = [t_procData['LATITUDE'], t_procData['LONGITUDE']]
            latlngList.append(t_latlongObj)

            # create the latlong all and latest file
            latlngFile = open(globals.LATLNG_FILE_PATH, "w")
            latlngFile.write(json.dumps(latlngList))
            latlngFile.close()


            # create the latlong all and latest file
            altFile = open(globals.ALTITUDE_FILE_PATH, "w")
            altFile.write(json.dumps(t_procData['ALTITUDE']))
            altFile.close()


            # add the data to the table
            tableHtmlGen.addData(t_procData)

            # create the HTML table and save it in table Data
            tableHtmlFile = open(globals.HTMLTABLE_FILE_PATH, "w")
            tableHtmlFile.write(tableHtmlGen.createTable())
            tableHtmlFile.close()

        nlogger_.log(nLogger.INFO, "Stopping")
        receiver.StopReceiving()

    except:
        nlogger_.log(nLogger.WARN, "EXCEPTION: {0}".format(sys.exc_info()[0]))
        receiver.StopReceiving()
        quit = True

