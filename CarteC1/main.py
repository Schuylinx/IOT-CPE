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
    json = "{"
    json += "\"source\":\""+CARD_ID+"\","
    json += "\"destination\":\""+CARD_DEST+"\","
    json += "\"password\":\""+NWK_IDFR+"\","
    json += "\"data\":["
    json += str(temperature())+","
    json += str(int((display.read_light_level()/255)*100))
    json += "]"
    json += "}"
    return json

def parseData(json):
    tmp = json[1:len(json)-1]
    tmp = tmp.replace("\"", "")
    tmp = tmp.split(",")
    temperature = tmp[3].split(":")[1].replace("[", "")
    light = tmp[4].replace("]", "")
    data = [temperature, light]
    return data

def parsePassword(json):
    tmp = json[1:len(json)-1]
    tmp = tmp.replace("\"", "")
    tmp = tmp.split(",")
    password = tmp[2].split(":")[1]
    return password
    
def checkPassword(password):
    return password == NWK_IDFR

while True:
    incomingJSON = radio.receive()
    if incomingJSON != None:
        parsePassword(incomingJSON)
        if checkPassword(parsePassword(incomingJSON)):
            add_text(0, 3, "vrai")
            order = parseData(incomingJSON)[0]
            if (order != DISP_ORD) and (order == "TL" or order == "LT"):
                DISP_ORD = order
    displayToScreen(DISP_ORD)
    
    radio.send(getJSONToSend())
    
    
    
    
    
    
    
    
    