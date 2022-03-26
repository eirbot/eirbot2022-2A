#!/bin/bash


ip=$(hostname -I) #recupere l'ip du site, fonctionne uniquement en local
ip=${ip: : -1}  #retire le caractere " " a la fin
port=8109   #port a ecrire a la main, celui de la derniere ligne de site.py

i=0
#boucle qui post les donnees de la camera
while [ 1 ]
do
    #remplacer le path
    data=$(python3 /mnt/c/Users/elias/Desktop/eirbot2022-2A/com/data_cam.py) 

    #ecrire l'ip de la rasp a la main
    curl "$ip:$port/pos_robot?robot=$data"

    #envoie la position des objets toutes les x secondes
    let "i=i+1"
    if [ $i -eq 3 ]
    then 
        data_obj=$(python3 /mnt/c/Users/elias/Desktop/eirbot2022-2A/com/data_cam.py) 
        curl "$ip:$port/pos_objet?objet=$data_obj"
        let "i=0"
    fi

    sleep 2 #data toutes les 3 sec
done

