# Program to control passerelle between Android application
# and micro-controller through USB tty
import time
import argparse
import signal
import sys
import socket
import socketserver
import serial
import threading
import json
import multiprocessing as mp
import string


PASERELLE_ID = "P"
PHONE_ID = "T"
CONTROLLEUR_ID = "C1"
HOST           = "0.0.0.0"
UDP_PORT       = 10000
MICRO_COMMANDS = ["TL" , "LT"]
FILENAME        = "values.txt"
LAST_VALUE      = "T:22,L:255"
PASSWORD = "ASecurePa$$19989/9"
dataStructure = {"source":"","destination":"","password":"","firstData":"","secondData":""}
TRAME_JSON = "{\"source\":\"%SOURCE\",\"destination\":\"%DESTINATION\",\"password\":\"%PASSWORD\",\"data\":[\"%D1\",\"%D2\"]}"


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        trame = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, trame))
        extractInformationFromData(trame)
        
        if dataStructure["firstData"] != "":
                if dataStructure["firstData"] in MICRO_COMMANDS: # Send message through UART
                        #sendUARTMessage(data)
                        print("Envoi à l'UART - Ordre demandé par téléphone " + dataStructure["firstData"])
                       
                elif dataStructure["firstData"] == "getValues()": # Sent last value received from micro-controller
                        with fileLock:
                                data = readOnFile()
                                if (data != ""):
                                        LAST_VALUE = createSendingTrame(PASERELLE_ID,PHONE_ID,PASSWORD,data.split(',')[0],data.split(',')[1])
                                        print(LAST_VALUE)
                                        socket.sendto(LAST_VALUE.encode('utf-8'), self.client_address) 
                                        print("Le téléphone demande les dernières values")
                                        # TODO: Create last_values_received as global variable      
                else:
                        print("Unknown message")


def listenSerial():
        while ser.isOpen() : 
                time.sleep(1)
                if (ser.inWaiting() > 0): # if incoming bytes are waiting 
                        data_str = (ser.read(ser.inWaiting())).decode()
                        data_str = data_str.replace('\x00','')
                        for trame in data_str.split("{"):
                                if (trame!=""):
                                        with fileLock:
                                                # Extraction of information 
                                                extractInformationFromData("{"+trame)
                                                # Write in the file
                                                # TODO Save Data in Data Base
                                                writeOnFile()
                                


class ThreadedSerialServer():
        pass                      

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
        pass


# send serial message 
SERIALPORT = "/dev/ttyACM0"
BAUDRATE = 115200
ser = serial.Serial()
fileLock = mp.Lock()
 
def initUART():        
        ser.port=SERIALPORT
        ser.baudrate=BAUDRATE
        ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        ser.parity = serial.PARITY_NONE #set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE
        #non-block read
        ser.timeout = 2              #timeout block read
        ser.xonxoff = False     #disable software flow control
        ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        ser.writeTimeout = 0     #timeout for write
        print ('Starting Up Serial Monitor')
        try:
                ser.open()
        except serial.SerialException:
                print("Serial {} port not available".format(SERIALPORT))
                exit()



def sendUARTMessage(msg):
    ser.write(msg)
    print("Message <" + msg + "> sent to micro-controller." )

# extract all information received in a specific JSON format
def extractInformationFromData(trameJSON):
        # extraction of the source
        dataStructure["source"] = (json.loads(trameJSON)["source"])
        # extraction of the destination
        dataStructure["destination"] = (json.loads(trameJSON)["destination"])
        # extraction of the password
        dataStructure["password"] = (json.loads(trameJSON)["password"])
        # extraction of data
        data = (json.loads(trameJSON)["data"])
        dataStructure["firstData"] = data[0]
        dataStructure["secondData"] = data[1]

def createSendingTrame(sourceId,destinationId,password,firstData,secondData):
        modifiedTrame = TRAME_JSON
        # Fill source
        modifiedTrame = modifiedTrame.replace("%SOURCE",sourceId)
        # Fill destination
        modifiedTrame = modifiedTrame.replace("%DESTINATION",destinationId)
        # Fill password
        modifiedTrame = modifiedTrame.replace("%PASSWORD",password)
        # Fill data
        modifiedTrame = modifiedTrame.replace("%D1",firstData)
        modifiedTrame = modifiedTrame.replace("%D2",secondData)
        return modifiedTrame




# Write last data in the file values.txt
def writeOnFile():
        # open file
        f= open(FILENAME,"w")
        # write data
        if (f.write(dataStructure["firstData"]+","+dataStructure["secondData"]) > 0):
                print("Données écrites")
        else:
                print("Données non écrites")
        # close file
        f.close()
def readOnFile():
        dataretrun = ""
        # open file
        f= open(FILENAME,"r")
        # read data
        data = f.readline()
        if (data!= ""):
                dataretrun = data
        # close file
        f.close()
        return dataretrun
# Main program logic follows:
if __name__ == '__main__':
        initUART()
        f= open(FILENAME,"a")
        print ('Press Ctrl-C to quit.')

        server = ThreadedUDPServer((HOST, UDP_PORT), ThreadedUDPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        serverSerial_thread = threading.Thread(target=listenSerial)
        serverSerial_thread.daemon = True
        server_thread.daemon = True

        try:
                server_thread.start()
                serverSerial_thread.start()
                print("Server started at {} port {}".format(HOST, UDP_PORT))
                while 1:"""ser.isOpen() : 
                        time.sleep(100)
                        if (ser.inWaiting() > 0): # if incoming bytes are waiting 
                                data_str = ser.read(ser.inWaiting()) 
                                #f.write(data_str)
                                LAST_VALUE = data_str
                                print(data_str)"""

        except (KeyboardInterrupt, SystemExit):
                server.shutdown()
                server.server_close()
                f.close()
                ser.close()
                exit()