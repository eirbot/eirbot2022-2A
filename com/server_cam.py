from flask import Flask, request
import numpy as np
import data_cam



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

#page d accueil car il en faut une 
@app.route('/')
def index():
    return 'elias la menace'

#page qui va envoyer les coordonnees calculees par la cam au robot
@app.route('/pos_robot', methods=['GET','POST'])
def pos_robot():
    if request.method=='GET':
        position = data_cam.EnvoiCoord()
        return str(position), 200 #ce qui est affiche dans la console de l emetteur (robot)

#a update pour les objets aussi
@app.route('/pos_objet', methods=['GET','POST'])
def pos_objet():
    if request.method=='GET':

        return "ca marche", 200 #ce qui est affiche dans la console de l emetteur (robot)

if __name__ == '__main__':
    app.run(debug=True, port=8109, host='0.0.0.0')