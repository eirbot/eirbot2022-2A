#include "Robot.hpp"

Robot::Robot(int x, int y, int t):_x(x),_y(y),_team(t){};

void Robot::set_position(int x, int y){
    _x = x;
    _y = y;
}

int Robot::get_x() const {
    return _x;
}

int Robot::get_y() const {
    return _y;
}

int Robot::get_team() const {
    return _team;
}