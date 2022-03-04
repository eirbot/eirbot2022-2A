#include "Movement.hpp"

void Movement::importantPoints(nodeList l)
{
    int derivative = 2;
    Node *node1 = l.at(0);
    for (int i = 1; i < l.size(); i++)
    {
        Node * node2 = l.at(i);
        int d = (node2->getY() - node1->getY())/(node2->getX() - node1->getX());
        if (d != derivative){
            movDescription.push_back(node1);
        }
    }
    movDescription.push_back(l.at(l.size()-1));
}

nodeList Movement::getMov(){
    return movDescription;
}