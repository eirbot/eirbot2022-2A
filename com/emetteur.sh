#!/bin/bash

ip=$(hostname -I) #recupere l'ip du site, fonctionne uniquement en local
ip=${ip: : -1}  #retire le caractere " " a la fin
port=8109   #port a ecrire a la main, celui de la derniere ligne de server.py

#boucle qui post les demandes de donnees
while [ 1 ]
do
    
    data="GET_ROBOT" #histoire de mettre un truc

    #ecrire l'ip de la rasp de la cam a la main
    curl "$ip:$port/pos_robot?robot=$data"

    sleep 2 #data toutes les 3 sec
done