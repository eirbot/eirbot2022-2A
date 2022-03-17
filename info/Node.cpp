#include "Node.hpp"

Node::Node(int v, int x, int y):val(v), x(x), y(y){}

Node::~Node(){
    delete previous;
}

void Node::setG(float i){
    g = i;
}

void Node::setH(float i){
    h = i;
}

void Node::setF(float i){
    f = i;
}

void Node::setVal(int v){
    val = v;
}

void Node::setDir(int d){
    direction = d;
}

void Node::setPrevious(Node* p){
    previous = p;
}

float Node::getF() const{
    return f;
}

float Node::getG() const{
    return g;
}

float Node::getH() const{
    return h;
}

int Node::getVal() const{
    return val;
}

int Node::getDir() const{
    return direction;
}

int Node::getX() const{
    return x;
}

int Node::getY() const{
    return y;
}

Node* Node::getPrevious() const{
    return previous;
}