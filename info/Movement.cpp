#include "Movement.hpp"

void Movement::importantPoints(nodeList l)
{
    int derivativeX = 2;
    int derivativeY = 2;
    Node *node1 = l.at(0);
    for (size_t i = 1; i < l.size(); i++)
    {
        Node *node2 = l.at(i);
        int dX = node2->getX() - node1->getX();
        int dY = node2->getY() - node1->getY();
        if (dX != derivativeX || dY != derivativeY)
        {
            derivativeX = dX;
            derivativeY = dY;
            movDescription.push_back(node1);
        }
        node1 = node2;
    }
    movDescription.push_back(l.at(l.size() - 1));
}

nodeList Movement::getMov()
{
    return movDescription;
}