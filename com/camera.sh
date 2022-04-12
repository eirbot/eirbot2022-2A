#!/bin/bash

##### VERSION LOCALE
ip=$(hostname -I) #recupere l'ip du site, fonctionne uniquement en local
ip=${ip: : -1}  #retire le caractere " " a la fin de la string
port=8109   #port a ecrire a la main, celui de la derniere ligne de server.py

curl "$ip:$port/pos_objet?objet=$1"


##### VERSION RASP

#Essayer de curl vers l'ip de la rasp du robot mais pas sur que ca marche 
#si pas de port de precise. Activer un port pour la reception ???
#sinon passer par des sockets ou autre moyen

#curl "$ip:$port/pos_objet?objet=$1"
