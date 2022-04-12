# Echange de données sans fil

Contenu : 
- [data_cam.py] : Génère des données aléatoires. A terme, enverra la position détectée avec la caméra.
- [server.py] : Le script qui permet de générer le site avec Flask. Si besoin, modifier le numéro de port à la dernière ligne du programme.
- [emetteur.sh] : Le script à exécuter pour émettre les données.
- [camera.sh] : Le script à exécuter pour recevoir les données.


Utilisation : 
- Ouvrir 2 terminaux et aller dans le bon répertoire.
- Rendre les fichiers [emetteur.sh] et [camera.sh] exécutables avec la commande `chmod +x nom_fichier.sh`.
- Avec un premier terminal, lancer le serveur (RASP Camera) avec la commande `./server.py`. Le site est désormais actif et est prêt à transmettre les données
- Avec un second terminal, modifier le fichier [emetteur.sh] avec la commande `nano emetteur.sh` par exemple. Il faut modifier dans la commande  `curl "$ip:$port/pos_robot?robot=$data"` les variables `$ip` pour écrire manuellement l'ip de la rasp de la caméra et aussi veiller à ce que le numéro de port `$port` soit le même que celui qui est activé pour le site. On le trouve dans le terminal lorsque l'on exécute [server.py] à la ligne suivante : 
```sh
 * Running on http://172.26.51.8:8109/ # ip = 172.26.51.8 et port = 8109
```
- De manière analogue, dans le fichier [camera.sh] écrire l'ip de la rasp du robot et le port en question (https://www.journaldev.com/34113/opening-a-port-on-linux).
- Une fois les modifications effectuées, exécuter l'émetteur.

Une fois que cela est fait, des données sont échangées périodiquement entre les machines. Les données émises et reçues sont des chaînes de caractères d'entiers.

Cela ne sert à rien d'ouvrir le site sur le navigateur, l'échange s'effectue correctement avec les terminaux.

[data_cam.py]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/data_cam.py>
[recepteur.py]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/server.py>
   [emetteur.sh]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/emetteur.sh>
   [camera.sh]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/camera.sh>
