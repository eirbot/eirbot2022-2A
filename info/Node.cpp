#include "Node.hpp"

Node::Node(int v, int x, int y):val(v), x(x), y(y){}

Node::~Node(){
    delete previous;
}

void Node::setG(int g){
    g = g;
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