# Echange de données sans fil

Contenu : 
- [data_cam.py] : Génère des données aléatoires. A terme, enverra la position détectée avec la caméra.
- [recepteur.py] : Le script qui permet de générer le site avec Flask. Si besoin, modifier le numéro de port à la dernière ligne du programme.
- [emetteur.sh] : Le script à exécuter pour émettre les données.
- [recepteur.sh] : Le script à exécuter pour recevoir les données.


Utilisation : 
- Ouvrir 2 terminaux et aller dans le bon répertoire
- Rendre les fichiers [emetteur.sh] et [recepteur.sh] exécutables  avec la commande `chmod +x nom_fichier.sh`.
- Avec un premier terminal, lancer le récepteur avec la commande `./recepteur.sh`. Le site est désormais actif et est prêt à recevoir les données
- Avec un second terminal, modifier le fichier [emetteur.sh] avec la commande `nano emetteur.sh` par exemple. Il faut modifier dans la commande  `curl "$ip:$port/pos_robot?robot=$data"` les variables `$ip` pour écrire manuellement l'ip de la rasp et aussi veiller à ce que le numéro de port est le même que celui qui est activé pour le site. On le trouve dans le terminal lorsque l'on exécute recepteur.sh à la ligne suivante : 
```sh
 * Running on http://172.26.51.8:8109/ # ip = 172.26.51.8 et port = 8109
```
- Une fois les modifications effectuées, exécuter l'émetteur.

Une fois que cela est fait, des données sont échangées périodiquement entre les machines. D'une part on envoie des données sous forme de chaîne de caractère et on récupère un tableau de bits correspondant à la conversion des entiers émis dans la chaîne de caractère. Le bit de poids fort est le plus à gauche et chaque entier est codé sur 9 bits.

Cela ne sert à rien d'ouvrir le site sur le navigateur, l'échange s'effectue correctement avec les terminaux.

[data_cam.py]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/data_camp.py>
[recepteur.py]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/emetteur.py>
   [emetteur.sh]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/emetteur.sh>
   [recepteur.sh]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/recepteur.sh>
