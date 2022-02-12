#include "Node.hpp"

Node::Node(int v, int x, int y):_val(v), _x(x), _y(y){}

Node::~Node(){
    delete _previous;
}

void Node::set_g(int g){
    _g = g;
}

void Node::set_previous(Node* p){
    _previous = p;
}

int Node::get_f() const{
    return _f;
}

int Node::get_g() const{
    return _g;
}

int Node::get_val() const{
    return _val;
}

int Node::get_x() const{
    return _x;
}

int Node::get_y() const{
    return _y;
}

Node* Node::get_previous() const{
    return _previous;
}