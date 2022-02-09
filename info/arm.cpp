#include "arm.hpp"
#include <cstdio>

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

int Arm::move(int idx_position) {
    setX(position[idx_position][0]);
    setY(position[idx_position][1]);
    printf("[Mode %d] La nouvelle position est %d,%d\n", idx_position, x_arm, y_arm);
    return 1;
}

int main(int argc, char* argv[]) {

    Arm a(2,4);
    printf("La position est %d,%d\n",a.getX(), a.getY());
    a.move(0);
    a.move(2);
    a.move(4);

    return 0;
}