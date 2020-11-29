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

def parsePassword (json):
    tmp = json[1:len(json)-1]
    tmp = tmp.replace("\"", "")
    tmp = tmp.split(",")
    password = tmp[2].split(":")[1]
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
    string = receive()
    if string != None:
        if checkPassWord(parsePassword(string)):
            boucle = True
        else:
            boucle = False
    if boucle:
        # Envoie du changement de sens -> C1
        radio.send(string)
    # Réception des valeurs [Temp, Lum] de C1
    incomingJSON = radio.receive()
    if incomingJSON != None:
        if checkPassWord(parsePassword(incomingJSON)):
            # Envoie des values -> P
            send(incomingJSON)