#!/usr/bin/python

import sys
import socket  # for socket
import time
import threading
import logging
import Queue


'''
UDPReceiver is a class which listens on an 
IP address, port number pair for ADBP messages to be received
and parsed them into a structure ADBP data . 
'''


class UDPReceiver:
    _packetSize = 1500
    _socketTimeout = 2.0
    _listeningIp = None
    _listeningPort = 0
    _queue = None
    _recvThread = None
    _stopFlag = False
    _socket = None

    ''' 
    queue is a Queue object which is a multi-producer and 
    multi-consumer queue for thread safe cases 
    '''

    def __init__(self, in_queue):
        self._queue = in_queue
        self.recvEvent_ = threading.Event()

    def SetBroadcastIP(self, in_ip):
        self._listeningIp = in_ip

    def SetBroadcastPort(self, in_port):
        self._listeningPort = in_port


    '''
    Start receiving, if it failed return False, else return True
    '''

    def StartReceiving(self):
        self._stopFlag = False
        self._recvThread = threading.Thread(target=self._receiveThread)

        # open up the socket
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.settimeout(self._socketTimeout)
        except:
            logging.error("error creating socket - %s" % (sys.exc_info()[1]))
            return False

        # bind the broadcast IP and port
        try:
            self._socket.bind((self._listeningIp, self._listeningPort))
        except:
            logging.error("error binding to IP:%s, Port:%s - %s" % (self._listeningIp
                                                                    , self._listeningPort, sys.exc_info()[1]))
            return False

        self._recvThread.start()
        return True


    ''' 
    Stop Receiving messages 
    '''

    def StopReceiving(self):
        self._stopFlag = True
        self.data_ = []

        time.sleep(1)

        if self._recvThread != None:
            if self._recvThread.isAlive():
                self._recvThread.join()

        if self._socket != None:
            self._socket.close()


    '''
    Receiving thread
    '''

    def _receiveThread(self):

        try:

            logging.info("Waiting for ADBP messages on port: %d",
                         self._listeningPort)

            # while true
            while True:

                if (self._stopFlag == True):
                    logging.info("Stopping receive thread")
                    break

                try:
                    # get received data, buffer size is 1024 bytes 
                    data, addr = self._socket.recvfrom(self._packetSize)

                    # continue on timeout
                except socket.timeout:
                    continue

                # i any other socket error occurs log and break
                except socket.error as msg:
                    logging.error("error with receiving data - %s" % (msg))
                    break

                # if data is empty, continue
                if not data:
                    logging.warn("received data is empty.")
                    continue

                # place item in queue
                self._queue.put(data)

                # log the packet to the logger
                logging.info("Received msg on port %d", self._listeningPort)

        except:
            logging.error("unhandled exception: %s" % sys.exc_info()[1])


if __name__ == '__main__':

    queue = Queue.Queue()

    receiver = UDPReceiver(queue)
    receiver.SetBroadcastIP("128.0.0.130")
    receiver.SetBroadcastPort(9070)

    if (receiver.StartReceiving() == False):
        print "error starting adbp receiver"
        exit(1)

    stopCounter = 50

    while (stopCounter != 0):
        item = queue.get()
        stopCounter -= 1

        print(item)

    print "Stopping"
    receiver.StopReceiving()
        

        
        
