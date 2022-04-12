from flask import Flask, request
import numpy as np
import data_cam
import subprocess
import shlex


#Convertit un entier 'int' en un tableau de bit de taille 'length'
#On prend length = 9 ici
def binConv(int, length):
    i=0
    tab = [0]*length
    while int >= 1:
        tab[length-i-1] = int%2
        i+=1
        int = int//2
    return tab

#conversion de la chaine postee sur le site en un tableau de bits [x y] de taille 2*length
#on renvoie sous forme de string aussi
def ReceptionCoord(str):
    str2 = str[1:len(str)-1]
    str3 = str2.split("'")
    str4 = str3[3]
    str5 = str4.split(",")
    str6 = np.hstack([binConv(int(str5[0]),9),binConv(int(str5[1]), 9)])
    str7 = np.hstack([int(str5[0]),int(str5[1])])
    if(str3[1] == 'robot'):
        print("c est un robot")
    elif(str3[1] == 'objet'):
        print("c est un objet")
    return np.array2string(str7)

app = Flask(__name__)

@app.route('/')
def index():
    return 'elias la menace'

@app.route('/pos_robot', methods=['GET','POST'])
def pos_robot():
    if request.method=='GET':
        position = data_cam.EnvoiCoord()
        script = "./camera.sh"
        command = "{} {}".format(script, str(position))
        subprocess.call(shlex.split(command)) #va executer le "script" avec en arg "position"

        return str(position) #ce qui est affiche dans la console de l emetteur, a remplacer par position

#ancienne version
@app.route('/pos_objet', methods=['GET','POST'])
def pos_objet():
    if request.method=='GET':

        return "ca marche" #ce qui est affiche dans la console de l emetteur, a remplacer par obj

if __name__ == '__main__':
    app.run(debug=True, port=8109, host='0.0.0.0')