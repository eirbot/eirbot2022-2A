#include "arm.hpp"
#include <cstdio>
#include <cstring>

/*--------------AJOUTER LES FLAGS END_MOVE ET AUTRE SI BESOIN--------------*/

//liste des differentes positions du bras
//0 = position initiale
//1 = détecter resistance
//2 = prendre palets
//3 = deposer palets
//4 = prendre statuette
//5 = deposer statuette

Arm::Arm(int pos_x, int pos_y)
{
    x_arm = pos_x;
    y_arm = pos_y;
}

int Arm::getX() {
    return x_arm;
    }

int Arm::getY() {
    return y_arm;
}

void Arm::setX(int pos_x) {
    x_arm = pos_x;
}

void Arm::setY(int pos_y) {
    y_arm = pos_y;
}

//On bouge le bras
int Arm::move(int idx_position) {
    setX(position[idx_position][0]);
    setY(position[idx_position][1]);
    printf("La nouvelle position est %d,%d\n\n", x_arm, y_arm);
    return 1;
}

//On choisit la position du bras
int Arm::set_pos(Arm a, int idx_position) {
    printf("Le bras passe en mode %s\n", pos_nom[idx_position]);
    a.move(idx_position);
    return 1;
}

int main(int argc, char* argv[]) {

    Arm a(2,4);
    printf("La position initiale est %d,%d\n\n",a.getX(), a.getY());
    a.set_pos(a,0);
    a.set_pos(a,2);

    return 0;
}