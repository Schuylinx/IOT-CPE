from microbit import *
import radio
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text

# config screen
initialize(pinReset=pin0)
clear_oled()
# config radio
radio.on()
radio.config(channel=1, length=251)

# constants
CARD_ID = "C1"
CARD_DEST = "C2"
DISP_ORD = "TL"
NWK_IDFR = "ASecurePa$$1998/9"

# functions
def displayToScreen(order): # order is a string
    if order == "TL":
        add_text(0, 0, "Temp : "+str(temperature())+" C  ")
        add_text(0, 1, "Lum : "+str(int((display.read_light_level()/255)*100))+" %  ")
    else:
        add_text(0, 0, "Lum : "+str(int((display.read_light_level()/255)*100))+" %  ")
        add_text(0, 1, "Temp : "+str(temperature())+" C  ")

def getJSONToSend():
    json = "{\"source\":\""+CARD_ID+"\",\"destination\":\""+CARD_DEST+"\",\"password\":\""+NWK_IDFR+"\",\"data\":["+str(temperature())+","
    json += str(int((display.read_light_level()/255)*100))+"]}"
    return json

def parseData(json):
    tmp = json[1:len(json)-1].replace("\"", "").split(",") 
    data = [tmp[3].split(":")[1].replace("[", ""), tmp[4].replace("]", "")] # [temperature, light]
    return data

def parsePassword(json):
    password = json[1:len(json)-1].replace("\"", "").split(",")[2].split(":")[1]
    return password

def checkPassword(password):
    return password == NWK_IDFR

while True:
    incomingJSON = radio.receive()
    if incomingJSON != None:
        #incomingJSON = decrypt(incomingJSON, 1)
        if checkPassword(parsePassword(incomingJSON)):
            order = parseData(incomingJSON)[0]
            if (order != DISP_ORD) and (order == "TL" or order == "LT"):
                DISP_ORD = order
    displayToScreen(DISP_ORD)
    radio.send(getJSONToSend())