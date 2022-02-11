#include "Node.hpp"

Node::Node(int v):_val(v){}

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

Node* Node::get_previous() const{
    return _previous;
}