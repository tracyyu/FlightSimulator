#!/usr/bin/python2.7
import json
import time
import csv
from datetime import datetime

from ADBPBinaryProcessor import *
from TableHTMLGenerator import *
import globals

inputFile = None
adbpBinProcessor = ADBPPacketProcessor()
tableHtmlGen = TableHTMLGenerator()
latlngList = []

receivedDataFile = None  # record the flight data in encrypted mode
csvLogFile = None  # decrypted log file that includes received data
previousDest = None
previousOrigin = None

try:

    # initialize global variables
    globals.init()

    # inputFile = open(globals.WWW_FOLDER + "serverApp/demo2.dat", "rb")
    inputFile = open(globals.SERVER_APP_DIR + "demo3.dat", "rb")

    inputData = ' '
    while inputData:

        # read first row of the data
        # extractedData = inputFile.read(290)
        inputData = inputFile.read(350)

        # processes the data and outputs a dictionary
        t_procData = adbpBinProcessor.Process(inputData)

        # if adbp processing returned null then break
        if t_procData is None:
            break

        # print t_procData

        # add up all the fuel items
        t_totalFuel = t_procData['FQTLOT'] + t_procData['FQTLIT'] + t_procData['FQTCT'] + \
                      t_procData['FQTRIT'] + t_procData['FQTROT'] + t_procData['FQTACT1'] + t_procData['FQTACT2'] + \
                      t_procData['FQTRCT'] + t_procData['FQTTRIMT'] + t_procData['EGT1'] + t_procData['EGT2']


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
            receivedDataFile.write(inputData)

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

        time.sleep(0.1)

finally:
    inputFile.close()

    # out.close()
