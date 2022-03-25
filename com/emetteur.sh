#!/bin/bash


ip=$(hostname -I) #recupere l'ip du site, fonctionne uniquement en local
ip=${ip: : -1}  #retire le caractere " " a la fin
port=8108   #port a ecrire a la main, celui de la derniere ligne de site.py

#boucle qui post les donnees de la camera
while [ 1 ]
do
    #remplacer le path
    data=$(python3 /mnt/c/Users/elias/Desktop/data_cam.py) 

    #ecrire l'ip de la rasp a la main
    curl "$ip:$port/pos_robot?robot=$data"

    sleep 2 #data toutes les 3 sec
done

