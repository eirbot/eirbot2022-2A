#include "Node.hpp"

Node::Node(int v, int x, int y):val(v), x(x), y(y){}

Node::~Node(){
    delete previous;
}

void Node::setG(int i){
    g = i;
}

void Node::setH(int i){
    h = i;
}

void Node::setF(int i){
    f = i;
}

void Node::setVal(int v){
    val = v;
}

void Node::setPrevious(Node* p){
    previous = p;
}

int Node::getF() const{
    return f;
}

int Node::getG() const{
    return g;
}

int Node::getH() const{
    return h;
}

int Node::getVal() const{
    return val;
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