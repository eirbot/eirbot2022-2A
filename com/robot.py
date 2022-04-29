import sys
import requests

#va envoyer une requete http a l adresse ci dessous et la valeur de retour 
#sera celle de la page pos_robot (server_cam.py ligne 45)
response = requests.get('http://'+sys.argv[1]+':'+sys.argv[2]+'/pos_robot')
#print(response.text)

#on transforme la chaine de caracteres en tableau
str1 = response.text.split(",")
pos=[int(str1[0]),int(str1[1])]
print(pos)