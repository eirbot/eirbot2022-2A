#include "Robot.hpp"

Robot::Robot(int x, int y, int t):x(x),y(y),team(t){};

void Robot::setPosition(int x, int y){
    x = x;
    y = y;
}

int Robot::getX() const {
    return x;
}

int Robot::getY() const {
    return y;
}

int Robot::getTeam() const {
    return team;
}