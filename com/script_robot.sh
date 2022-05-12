#!/bin/bash

ip=$(hostname -I) #recupere l'ip du site, fonctionne uniquement en local, noter celle de la rasp de la cam a la main
ip=${ip: : -1}  #retire le caractere " " a la fin
port=8109   #port a ecrire a la main, celui de la derniere ligne de server_cam.py

#boucle qui gere les envois receptions de requetes http
while [ 1 ]
do
    
    #on execute le script robot.py avec les args $ip et $port (remplacer le path)
    python3 /mnt/c/Users/elias/Desktop/eirbot2022-2A/com/robot.py $ip $port

    sleep 2 #data toutes les 3 sec
done
