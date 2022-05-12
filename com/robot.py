import sys
import requests

#va envoyer une requete http a l adresse ci dessous et la valeur de retour 
#sera celle de la page pos_robot (server_cam.py ligne 45)
response = requests.get('http://'+sys.argv[1]+':'+sys.argv[2]+'/pos_robot')
#print(response.text)

if(int(sys.argv[1]) == 1):
    response = requests.get('http://'+sys.argv[2]+':'+sys.argv[3]+'/pos_objet')

    str1 = response.text.split(",")
    pos_fin = [0]*len(str1)
    for i in range(len(str1)):
        pos_fin[i] = int(str1[i])
    print("objets")
#sortie = un tableau de taille variable, 1x(2*Nb_objet) avec les (x,y) de chaque objet
#faire un programme pour le traitement d'un objet parmi ceux detectes, 
#prendre le plus proche par exemple et éliminer les autres

print(pos_fin)

