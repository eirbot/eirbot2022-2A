# Echange de données sans fil

Contenu : 
- [data_cam.py] : Génère des données aléatoires. A terme, enverra la position détectée avec la caméra.
- [server_cam.py] : Le script à exécuter qui permet de générer le site avec Flask. Si besoin, modifier le numéro de port à la dernière ligne du programme.
- [script_robot.sh] : Le script à exécuter pour le robot.
- [robot.py] : Le script qui permet de faire les requêtes et obtenir les positions.


Utilisation : 
- Ouvrir 2 terminaux et aller dans le bon répertoire.
- Rendre le [script_robot.sh] exécutable avec la commande `chmod +x nom_fichier.sh`.
- Avec un premier terminal, lancer le serveur (RASP Camera) avec la commande `python3 server_cam.py`. Le site est désormais actif et est prêt à transmettre les données
- Avec un second terminal, modifier le fichier [script_robot.sh] avec la commande `nano script_robot.sh` par exemple. Il faut modifier les variables `$ip` pour écrire manuellement l'ip de la rasp de la caméra et aussi veiller à ce que le numéro de port `$port` soit le même que celui qui est activé pour le site. On le trouve dans le terminal lorsque l'on exécute [server_cam.py] à la ligne suivante : 
```sh
 * Running on http://172.26.51.8:8109/ # ip = 172.26.51.8 et port = 8109
```
- Une fois les modifications effectuées, exécuter le script du robot ([script_robot.sh]).

Une fois que cela est fait, des données sont échangées périodiquement entre les machines. Les données reçues sont des chaînes de caractères qui sont transformés en tableau dans [robot.py].

Cela ne sert à rien d'ouvrir le site sur le navigateur, l'échange s'effectue correctement avec les terminaux.

[data_cam.py]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/data_cam.py>
[server_cam.py]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/server_cam.py>
   [script_robot.sh]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/script_robot.sh>
   [robot.py]: <https://github.com/eirbot/eirbot2022-2A/blob/main/com/robot.py>
