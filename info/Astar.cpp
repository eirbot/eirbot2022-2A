#include "Astar.hpp"
#include <math.h>
#include <string>

Astar::Astar(Node *n, nodeList *nliste, Table t) : start(n), end(nliste), map(t) {}

int Astar::distance(Node *n1, Node *n2)
{
    return sqrt(abs(n2->getX() - n1->getX()) + abs(n2->getY() - n1->getY()));
}

void Astar::findPath()
{
    Node *current = end->front();
    path.push_back(current);
    while (current != start)
    {
        current = current->getPrevious();
        path.push_back(current);
    }
}

nodeList Astar::findNeighbor(Node *n)
{
    nodeList neighbor;
    int x = n->getX();
    int y = n->getY();
    if (x > 0)
    {
        neighbor.push_back(map.nodeAt(x - 1, y));
    }
    if (x < map.getWidth() - 1)
    {
        neighbor.push_back(map.nodeAt(x + 1, y));
    }
    if (y > 0)
    {
        neighbor.push_back(map.nodeAt(x, y - 1));
    }
    if (y < map.getHeight() - 1)
    {
        neighbor.push_back(map.nodeAt(x, y + 1));
    }
    if (x > 0 && y > 0)
    {
        neighbor.push_back(map.nodeAt(x - 1, y - 1));
    }
    if (x > 0 && y < map.getHeight() - 1)
    {
        neighbor.push_back(map.nodeAt(x + 1, y + 1));
    }
    if (x < map.getWidth() - 1 && y > 0)
    {
        neighbor.push_back(map.nodeAt(x - 1, y + 1));
    }
    if (x < map.getWidth() - 1 && y < map.getHeight() - 1)
    {
        neighbor.push_back(map.nodeAt(x + 1, y - 1));
    }
    for (int i = 0; i < neighbor.size(); i++)
    {
        if (neighbor[i]->getVal() != 0)
        {
            neighbor.erase(neighbor.begin() + i);
            i--;
        }
    }
    return neighbor;
}

bool Astar::isNodeOnList(Node *n, const nodeList &nliste)
{
    for (Node *node : nliste)
    {
        if (node->getX() == n->getX() && node->getY() == n->getY())
        {
            return true;
        }
    }
    return false;
}

int Astar::findPlace(Node *n, const nodeList &nliste)
{
    for (int i = 0; i < nliste.size(); i++)
    {
        if (nliste[i] == n)
        {
            return i;
        }
    }
    return -1;
}

Node *Astar::findLowestCostNode(const nodeList &nliste)
{
    Node *lowestCostNode = nullptr;
    int lowestCost = -1;
    for (Node *node : nliste)
    {
        if (node->getF() < lowestCost || lowestCost == -1)
        {
            lowestCost = node->getF();
            lowestCostNode = node;
        }
    }
    return lowestCostNode;
}

void Astar::printPath(Table& map, nodeList* path, nodeList* openList, nodeList* closedList) {
    file.open("map.ppm");
    file << "P3\n" << map.getHeight() << " " << map.getWidth() << "\n255\n";
    for (int i = 0; i < map.getHeight(); i++) {
        for (int j = 0; j < map.getWidth(); j++) {
            if (isNodeOnList(map.nodeAt(j,i), *path)) {
                file << "255 0 0 ";
            } else if (isNodeOnList(map.nodeAt(j,i), *openList)) {
                file << "0 0 255 ";
            } else if (isNodeOnList(map.nodeAt(j,i), *closedList)) {
                file << "0 255 0 ";
            } else if (map.nodeAt(j,i)->getVal() != 0) {
                file << "0 0 0\n";
            } else {
                file << "255 255 255\n";
            }
        }
    }
    file.close();
}