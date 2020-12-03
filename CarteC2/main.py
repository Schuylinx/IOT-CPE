from microbit import *
import radio

 

# Constantes
CARD_ID = "C2"
CARD_DEST = "P"
DISP_ORDER = "TL"
NWK_IDFR = "ASecurePa$$1998/9"
ASCII = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
# Config Radio
radio.on()
radio.config(channel=1, length=251)
# Config Serial
uart.init(baudrate=115200)

 

def parsePassword (json):
    tmp = json[1:len(json)-1]
    tmp = tmp.replace("\"", "")
    tmp = tmp.split(",")
    password = (tmp[2].split(":"))[1]
    return password

 

def checkPassWord (password):
    return password == NWK_IDFR

 

def crypte(msg): # Vigenere
    alpha = ASCII
    cle = ")ow2&9@>-b>ogg*t.:e*,mk>"
    res = ''
    i = 0
    for caractere in msg:
        debut = alpha.find(cle[i])
        pos = alpha.find(caractere)
        indice = pos+debut
        if indice > 99:
            indice = indice%100
        res += alpha[indice]
        i += 1
        if i >= len(cle):
            i = 0
    return res

 

def decrypte(msg): # Vigenere
    alpha = ASCII
    cle = ")ow2&9@>-b>ogg*t.:e*,mk>"
    res = ''
    i = 0
    for caractere in msg:
        debut = alpha.find(cle[i])
        pos = alpha.find(caractere)
        indice = pos-debut
        res += alpha[indice]
        i += 1
        if i >= len(cle):
            i = 0
    return res

 

def send(m):
    b = []
    for c in m:
        b.append(ord(c))
    d = bytes(b)
    uart.write(d)

 

def receive():
    if uart.any():
        m = uart.read()
        s = ""
        for b in m:
            s = s + chr(b)
        return s

 


string = ""
stringSend = ""
boucle = False
while True:
    # Réception du changement de sens -> P
    string = receive()
    if string != None:
        if(DISP_ORDER=="TL"):
            DISP_ORDER="LT"
        else:
            DISP_ORDER="TL"
        if (len(string.split(":")) == 5):
            if checkPassWord(parsePassword(string)):
                stringSend = string
        else:
            stringSend = "{\"source\":\"C2\",\"destination\":\"C1\",\"password\":\"ASecurePa$$1998/9\",\"data\":[\"ORDER\",\"NULL\"]}"
            stringSend = stringSend.replace("ORDER",DISP_ORDER)
    if stringSend != "":
        # Envoie du changement de sens -> C1
        radio.send(stringSend)
    # Réception des valeurs [Temp, Lum] de C1
    incomingJSON = radio.receive()
    if incomingJSON != None:
        if checkPassWord(parsePassword(incomingJSON)):
            # Envoie des values -> P
            send(incomingJSON)
    sleep(2000)