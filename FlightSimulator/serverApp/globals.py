#!/usr/bin/env python

def init():
    global WWW_FOLDER
    global TEMPLATE_DIR
    global SERVER_APP_DIR
    global HISTORY_DIR
    global LATLNG_FILE_PATH
    global ALTITUDE_FILE_PATH
    global HTMLTABLE_FILE_PATH
    global PORT_NUMBER
    global RECEIVE_TIMEOUT_SEC
    global ERROR_FILE_PATH

    WWW_FOLDER = '/Sites/tracyyu/demo/'
    TEMPLATE_DIR = WWW_FOLDER + '/template/'
    SERVER_APP_DIR = WWW_FOLDER + '/serverApp/'
    HISTORY_DIR = SERVER_APP_DIR + '/receivedData/'

    LATLNG_FILE_PATH = WWW_FOLDER + "mapData/latlng.json"
    ALTITUDE_FILE_PATH = WWW_FOLDER + "mapData/alt.json"
    HTMLTABLE_FILE_PATH = WWW_FOLDER + "tableData/adbpTable.html"
    ERROR_FILE_PATH = WWW_FOLDER + "errorData/errorMessage.html"

    PORT_NUMBER = 9070
    RECEIVE_TIMEOUT_SEC = 10