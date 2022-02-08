#include "Sample.hpp"

Sample::Sample(int x, int y, int c):_x(x),_y(y),_color(c){};

void Sample::set_position(int x, int y){
    _x = x;
    _y = y;
}

int Sample::get_x() const {
    return _x;
}

int Sample::get_y() const {
    return _y;
}

int Sample::get_color() const {
    return _color;
}