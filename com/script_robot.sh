#!/bin/bash

ip=$(hostname -I) #recupere l'ip du site, fonctionne uniquement en local, noter celle de la rasp de la cam a la main
ip=${ip: : -1}  #retire le caractere " " a la fin
port=8109   #port a ecrire a la main, celui de la derniere ligne de server_cam.py

#boucle qui gere les envois receptions de requetes http
i=0
while [ 1 ]
do
    
    #on execute le script robot.py avec les args $ip et $port (remplacer le path)
    python3 /mnt/c/Users/elias/Desktop/eirbot2022-2A/com/robot.py 0 $ip $port #0 pour le robot

    let "i=i+1"
    if [ $i -eq 3 ]
    then 
        python3 /mnt/c/Users/elias/Desktop/eirbot2022-2A/com/robot.py 1 $ip $port #1 pour les objets
        let "i=0"
    fi

    sleep 2 #data toutes les 3 sec
done