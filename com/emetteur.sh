#!/bin/bash

ip=$(hostname -I) #recupere l'ip du site, fonctionne uniquement en local
ip=${ip: : -1}  #retire le caractere " " a la fin
port=8109   #port a ecrire a la main, celui de la derniere ligne de server.py

#boucle qui post les demandes de donnees
while [ 1 ]
do
    
    python3 /mnt/c/Users/elias/Desktop/eirbot2022-2A/com/robot.py $ip $port

    sleep 2 #data toutes les 3 sec
done