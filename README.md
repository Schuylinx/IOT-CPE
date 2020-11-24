# Mini projet IOT, Novembre 2020
---
## Equipe 5 : *Ferrer, Contini, Dugue, Gasparini*
---

## Bienvenue sur le repo de l'équipe 5 !
Dans le cadre de notre formation d'ingénieur "Informatique & Réseaux de Communication (IRC)" dispensée à CPE, nous devons réaliser un mini projet d'IOT. Le but de ce projet est de mettre en place une architecture informatique orientée IOT composée de deux cartes BBC micro:bit, l'une jouant le rôle de capteurs (lumière et température), l'autre de passerelle connectée à internet. Le réseau de capteurs peut être commandé à distance depuis un smartphone Android.

### 1. Commencer
- Travailler sous Windows 10 :
    - Télécharger et installer [mu editor](https://codewith.mu/en/download)
    - Clôner ce repository dans le dossier de code de mu editor (C:\Users\Username\mu_code)
    - Ca y est ! vous êtes prêts à travailler !
    
### 2. Branchement micro:bit <-> écran
- Fil rouge <-> PIN 0
- Fil orange <-> PIN 19
- Fil bleu <-> 3V
- Fil vert <-> 0V
- Fil jaune <-> PIN 20

### 3. Communication interne
La communication dans le système se fait en JSON, pour des raisons de facilité d'implémentation et de rapidité au sein de ce module, la sécurité de notre système sera assurée par plusieurs facteurs d'authentification :
- Un mot de passe communiqué en dur à chaque instance et stocké localement sur les différents intervenants (< **PASSWORD** >)
- Un chiffrement / hachage sur le JSON, processus défini en amont et nécessaire à l'interprétation des données
- La validation de la structure du JSON 

Pour s'assurer du bon traitement à effectuer sur les acteurs du système un duo source/destination a été mis en place. 

La définition des acteurs associés :

| ID | Description |
|--|--|
| C1 | Carte Micro-bit 1, capteur thermomètre et luminosité |
| C2 | Carte Micro-bit 2, centre de contrôle du système, lien entre C1 et P |
| P | Passerelle, serveur manipulant la base de donnée (fichier dans le cadre de ce module) |
| T | Application Android mise en place sur le téléphone (ou émulateur) |

La dualité mise en place *(dans un système mono-capteur C2 est simplement un intermédiaire)* :

| Source | Destination | Description |
|--|--|--|
| C1 | P | Envoi des données de Température + Luminosité |
| P | C1 | Transmission de l'ordre d'affichage de Température + Luminosité |
| T | P | Envoi de l'ordre d'affichage de Température + Luminosité OU demande de valeurs |
| P | T | Transmission des données de Température + Luminosité |

Pour définir les échanges dans le système un champ < data >  est mis en place dans le JSON. Il s'agit d'un tableau de 2 entiers dont les détails d'implémentation sont précisés ci-dessous :

| Source | Destination | Indice 0 | Indice 1
|--|--|--|--|
| C1 | P | int : Température | int : Luminosité
| P | C1 | string : "TL" ou string : "LT" | ""
| T | P | string : "TL" ou string : "LT" (pour inverser l'ordre) OU string : "getValues()" (pour récupérer les valeurs) | ""
| P | T | int : Température | int : Luminosité

La structure du JSON est la suivante :

```json
{
	source : < ID >,
	destination : < ID >,
	password : < PASSWORD >,
	data : [< DATA >]
}
```

## Exemples de requêtes :

Communication des valeurs des capteurs (capteur vers passerelle) :
```json
{
	source : "C1",
	destination : "P",
	password : "MDPtrèsSécurisé9998",
	data : [22,53]
}
```

Communication des valeurs des capteurs (passerelle vers téléphone) :
```json
{
	source : "P",
	destination : "T",
	password : "MDPtrèsSécurisé9998",
	data : [22,53]
}
```

Demande du changement de l'ordre des capteurs :
```json
{
	source : "T",
	destination : "P",
	password : "MDPtrèsSécurisé9998",
	data : ["TL",""]
}
```

Communication du changement de l'ordre des capteurs :
```json
{
	source : "P",
	destination : "C1",
	password : "MDPtrèsSécurisé9998",
	data : ["TL",""]
}
```

Demande des valeurs des capteurs à la passerelle :
```json
{
	source : "T",
	destination : "P",
	password : "MDPtrèsSécurisé9998",
	data : ["getValues()",""]
}
```



