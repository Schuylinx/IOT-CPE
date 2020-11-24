# Choix du chiffrement des données :

Le chiffrement par césare ne transformait pas les caractères hors alphabet afin de pouvoir les retrouver dans la fonction de décrypte.
Donc j'ai réaliser une nouvelle fonction d'encryption, Vigenère.
Avec une clef privé et un alphabet total.


## Principe Chiffrement

Pour chaque caractère du message que l'on veut chiffrer:
 - Il trouve la position de ce caractères dans l'alphabet,
 - il va aussi prendre la position du caractère de la clef en phase (position modulo taille de la clef) dans l'alphabet, 
 - et la somme des deux positions, modulo taille de l'alphabet, est le nouveau caractère

## Principe Déchiffrement

C'est le même principe que dans l'autre sens, por chaque caractère du message que l'on veut déchiffrer :
 - On prend la position du caractère dans l'alphabet,
 - On prend la position du carctère de la clef en phase,
 - On fait cette fois la soustraction de la position du char chiffré par positon du carcatère de la clef, 
 - On retrouve ainsi le carctère non chiffré.

## Code Crypte:

    def Crypte(msg):
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

## Code Décrypte

    def Decrypte(msg):
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


