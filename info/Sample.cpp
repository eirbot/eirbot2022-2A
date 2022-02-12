#include "Sample.hpp"

Sample::Sample(int x, int y, int c):x(x),y(y),color(c){};

void Sample::setPosition(int x, int y){
    x = x;
    y = y;
}

int Sample::getX() const {
    return x;
}

int Sample::getY() const {
    return y;
}

int Sample::getColor() const {
    return color;
}