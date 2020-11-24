from microbit import *
import radio

# Constantes
CARD_ID = "C2"
CARD_DEST = "P"
NWK_IDFR = "ASecurePa$$1998/9"
ASCII = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
# Config Radio
radio.on()
radio.config(channel=1, length=251)
# Config Serial
uart.init(baudrate=115200)

def ParsePassword (json):
    tmp = json[1:len(json)-1]
    tmp = tmp.replace("\"", "")
    tmp = tmp.split(",")
    password = tmp[2].split(":")[1]
    return password

def checkPassWord (password):
    return password == Crypte(NWK_IDFR)

def Crypte(msg): # Cesare
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

def Decrypte(msg): # Cesare
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

def Send(m):
    if uart.any():
        b = []
        for c in m:
            b.append(ord(c))
        d = bytes(b)
        uart.write(d)

def Receive():
    if uart.any():
        m = uart.readline()
        s = ""
        for b in m:
            s = s + chr(b)
        return s

#string = "{\"source\":\"C1\",\"destination\":\"C2\",\"pwd\":\"ASecurePa$$1998/9\",\"data\":[\"LT\",NULL]}"
string = ""
boucle = False
while True:
    # Réception du changement de sens -> P
    string = Receive()
    if string != None:
        if checkPassWord(parsePassword(Decrypte(string))):
            boucle = True
    if boucle:
        # Envoie du changement de sens -> C1
        radio.send(Crypte(string))
    # Réception des valeurs [Temp, Lum] de C1
    incomingJSON = radio.receive()
    if incomingJSON != None:
        if checkPassWord(parsePassword(Decrypte(incomingJSON))):
            # Envoie des values -> P
            Send(incomingJSON)