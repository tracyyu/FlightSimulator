#!/usr/bin/env python
import collections
from jinja2 import Environment, FileSystemLoader
import globals


class TableHTMLGenerator:

    tableHtmlTemplate = 'table.html'

    def __init__(self):
        # initialize global variables
        globals.init();

    # dictionary to convert Format A717 names to caption names
    CaptionListTimeFrame = {
        "TIME": "Time",
        "FrameCounter": "Frame Counter"
    }

    CaptionListFlightSum = {
        "ACFTREG": "Aircraft Registration",
        "FLTNUM": "Flight Number",
        "ORIGIN": "Departure Airport",
        "DESTINATION": "Destination Airport"
    }

    CaptionListFlightStat = {
        "FLTPHASE": "Flight Phase",
        "LATITUDE": "Latitude",
        "LONGITUDE": "Longitude",
        "ALTITUDE": "Altitude",
        "CAS": "Computed Airspeed",
        "GNDSPEED": "Ground Speed",
        "MACH": "Mach",
        "HDG": "True/Magnetic Heading",
        "HDGSEL": "Heading Selection",
        "VERTSPEED": "Vertical Speed",
        "WINDSPEED": "Windspeed",
        "WINDDIRT": "Wind Direction"
    }

    CaptionListAircraftStat = {
        "TOTFUEL": "Fuel on Board",
        "N11": "Engine 1 N1",
        "N12": "Engine 1 N2",
        "N21": "Engine 2 N1",
        "N22": "Engine 2 N2",
        "MWCPFWC1": "Master Warn 1 - Capt",
        "MWFOFWC1": "Master Warn 1 - FO",
        "MCCPFWC1": "Master Caution 1 - Capt",
        "MCFOFWC1": "Master Caution 1 - FO",
        "MWCPFWC2": "Master Warn 2 - Capt",
        "MWFOFWC2": "Master Warn 2 - FO",
        "MCCPFWC2": "Master Caution 2 - Capt",
        "MCFOFWC2": "Master Caution 2 - FO",
        "ENG1LOP": "Engine 1 Oil",
        "ENG2LOP": "Engine 2 Oil",
        "EGT1" : "Engine 1 Temperature",
        "EGT2" : "Engine 2 Temperature"
    }

    # where the parsed date will be held
    dataTimeFrame = []
    dataFlightSum = []
    dataFlightStat = []
    dataAircraftStat = []


    # appends the parsed data into a list
    def addData(self, parsedData):

        # Clears previously stored data
        self.dataTimeFrame = []
        self.dataFlightSum = []
        self.dataFlightStat = []
        self.dataAircraftStat = []

        # create a temporary dictionary in the order the key/value will be added
        tempOrderDicTimeFrame = collections.OrderedDict()
        tempOrderDicFlightSum = collections.OrderedDict()
        tempOrderDicFlightStat = collections.OrderedDict()
        tempOrderDicAircraftStat = collections.OrderedDict()

        # store time as the first key/value pair
        if "TIME" in parsedData:
            tempOrderDicTimeFrame["TIME"] = parsedData["TIME"]

        if "FrameCounter" in parsedData:
            tempOrderDicTimeFrame["FrameCounter"] = parsedData["FrameCounter"]

        # store all the static, flight summary value pairs
        if "ACFTREG" in parsedData:
            tempOrderDicFlightSum["ACFTREG"] = parsedData["ACFTREG"]

        if "FLTNUM" in parsedData:
            tempOrderDicFlightSum["FLTNUM"] = parsedData["FLTNUM"]

        if "ORIGIN" in parsedData:
            tempOrderDicFlightSum["ORIGIN"] = parsedData["ORIGIN"]

        if "DESTINATION" in parsedData:
            tempOrderDicFlightSum["DESTINATION"] = parsedData["DESTINATION"]

        # store all the dynamic, flight status value pairs
        if "FLTPHASE" in parsedData:
            tempOrderDicFlightStat["FLTPHASE"] = parsedData["FLTPHASE"]

        if "LATITUDE" in parsedData:
            tempOrderDicFlightStat["LATITUDE"] = parsedData["LATITUDE"]

        if "LONGITUDE" in parsedData:
            tempOrderDicFlightStat["LONGITUDE"] = parsedData["LONGITUDE"]

        if "ALTITUDE" in parsedData:
            tempOrderDicFlightStat["ALTITUDE"] = parsedData["ALTITUDE"]





        if "CAS" in parsedData:
            tempOrderDicFlightStat["CAS"] = parsedData["CAS"]

        if "GNDSPEED" in parsedData:
            tempOrderDicFlightStat["GNDSPEED"] = parsedData["GNDSPEED"]

        if "MACH" in parsedData:
            tempOrderDicFlightStat["MACH"] = parsedData["MACH"]

        if "HDG" in parsedData:
            tempOrderDicFlightStat["HDG"] = parsedData["HDG"]





        if "HDGSEL" in parsedData:
            tempOrderDicFlightStat["HDGSEL"] = parsedData["HDGSEL"]

        if "VERTSPEED" in parsedData:
            tempOrderDicFlightStat["VERTSPEED"] = parsedData["VERTSPEED"]

        if "WINDSPEED" in parsedData:
            tempOrderDicFlightStat["WINDSPEED"] = parsedData["WINDSPEED"]

        if "WINDDIRT" in parsedData:
            tempOrderDicFlightStat["WINDDIRT"] = parsedData["WINDDIRT"]





        # storall all the dynamic, aircraft status value pairs
        if "TOTFUEL" in parsedData:
            tempOrderDicAircraftStat["TOTFUEL"] = parsedData["TOTFUEL"]

        if "N11" in parsedData:
            tempOrderDicAircraftStat["N11"] = parsedData["N11"]

        if "N12" in parsedData:
            tempOrderDicAircraftStat["N12"] = parsedData["N12"]

        if "N21" in parsedData:
            tempOrderDicAircraftStat["N21"] = parsedData["N21"]

        if "N22" in parsedData:
            tempOrderDicAircraftStat["N22"] = parsedData["N22"]





        if "MWCPFWC1" in parsedData:
            tempOrderDicAircraftStat["MWCPFWC1"] = parsedData["MWCPFWC1"]

        if "MWFOFWC1" in parsedData:
            tempOrderDicAircraftStat["MWFOFWC1"] = parsedData["MWFOFWC1"]

        if "MCCPFWC1" in parsedData:
            tempOrderDicAircraftStat["MCCPFWC1"] = parsedData["MCCPFWC1"]

        if "MCFOFWC1" in parsedData:
            tempOrderDicAircraftStat["MCFOFWC1"] = parsedData["MCFOFWC1"]




        if "MWCPFWC2" in parsedData:
            tempOrderDicAircraftStat["MWCPFWC2"] = parsedData["MWCPFWC2"]

        if "MWFOFWC2" in parsedData:
            tempOrderDicAircraftStat["MWFOFWC2"] = parsedData["MWFOFWC2"]

        if "MCCPFWC2" in parsedData:
            tempOrderDicAircraftStat["MCCPFWC2"] = parsedData["MCCPFWC2"]

        if "MCFOFWC2" in parsedData:
            tempOrderDicAircraftStat["MCFOFWC2"] = parsedData["MCFOFWC2"]


        if "ENG1LOP" in parsedData:
            tempOrderDicAircraftStat["ENG1LOP"] = parsedData["ENG1LOP"]

        if "ENG2LOP" in parsedData:
            tempOrderDicAircraftStat["ENG2LOP"] = parsedData["ENG2LOP"]

        if "EGT1" in parsedData:
            tempOrderDicAircraftStat["EGT1"] = parsedData["EGT1"]

        if "EGT2" in parsedData:
            tempOrderDicAircraftStat["EGT2"] = parsedData["EGT2"]


        #tempOrderDic["ENG1LOP"] = parsedData["ENG1LOP"]
        #tempOrderDic["ENG2LOP"] = parsedData["ENG2LOP"]

        # Loop through tempOrderDicTimeFrame and 
        # replace key with those in CaptionList
        changedTimeFrameDic = collections.OrderedDict()
        for key, value in tempOrderDicTimeFrame.items():
            changedTimeFrameDic[self.CaptionListTimeFrame[key]] = value

        # Loop through tempOrderDicFlightSum and 
        # replace key with those in CaptionList
        changedFlightSumDic = collections.OrderedDict()
        for key, value in tempOrderDicFlightSum.items():
            changedFlightSumDic[self.CaptionListFlightSum[key]] = value

        # Loop through tempOrderDicFlightStat and 
        # replace key with those in CaptionList
        changedFlightStatDic = collections.OrderedDict()
        for key, value in tempOrderDicFlightStat.items():
            changedFlightStatDic[self.CaptionListFlightStat[key]] = value

            # Loop through tempOrderDicAircraftStat and
        # replace key with those in CaptionList
        changedAircraftStatDic = collections.OrderedDict()
        for key, value in tempOrderDicAircraftStat.items():
            changedAircraftStatDic[self.CaptionListAircraftStat[key]] = value

        # appends the ordered dictionaries into the list for the categories data
        self.dataTimeFrame.append(changedTimeFrameDic)
        self.dataFlightSum.append(changedFlightSumDic)
        self.dataFlightStat.append(changedFlightStatDic)
        self.dataAircraftStat.append(changedAircraftStatDic)

    def createTable(self):

        # return string
        rtnStr = ""

        # create an environment routed to the template path
        env = Environment(loader=FileSystemLoader(globals.TEMPLATE_DIR))

        # get the templates in the template directory
        templateTable = env.get_template(self.tableHtmlTemplate)

        # creates a string of the html datatable
        t_tableData = ""
        t_tableData += (templateTable.render(TimeFrame=self.dataTimeFrame,
                                             FlightSum=self.dataFlightSum,
                                             FlightStat=self.dataFlightStat,
                                             AircraftStat=self.dataAircraftStat))

        # return string 
        rtnStr += t_tableData

        # returns the table html
        return rtnStr



