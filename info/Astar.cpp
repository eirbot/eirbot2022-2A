#include "Astar.hpp"
#include <string>
#include <math.h>

Astar::Astar(Node *n, nodeList nlist, Table *t) : start(n), end(nlist), map(t) {
    initialize();
}

int Astar::distance(Node *n1, Node *n2)
{
    return (n2->getX() - n1->getX()) * (n2->getX() - n1->getX()) + (n2->getY() - n1->getY()) * (n2->getY() - n1->getY());
}

Astar::~Astar() {}

void Astar::initialize()
{
    for (int i = 0; i < map->getHeight(); i++)
    {
        for (int j = 0; j < map->getWidth(); j++)
        {
            Node *n = map->nodeAt(j, i);
            n->setH(distance(n, end.front()));
        }
    }
}

void Astar::searchPath()
{
    Node *current = closed_list[closed_list.size() - 1];
    while (current != nullptr)
    {
        path.push_back(current);
        current = current->getPrevious();
    }
}

nodeList Astar::findPath()
{
    Node *current = start;
    current->setG(0);
    current->setF(current->getG() + current->getH());
    current->setPrevious(nullptr);
    open_list.push_back(current);
    closed_list.push_back(current);
    //int i =0;
    while (!isNodeOnList(current, end))
    {
        /*i++;
        if(i<10){
        printf("%i\n",i);
        printf("x : %i, y : %i\n", current->getX(), current->getY());
        printf("%i\n", current->getF());
        printf("%i\n", current->getG());
        printf("%i\n", current->getH());
        printList(open_list);
        }*/
        nodeList neighbors = findNeighbor(current);
        for (Node *neighbor : neighbors)
        {
            if (neighbor != nullptr)
            {
                if (!isNodeOnList(neighbor, closed_list))
                {
                    neighbor->setG(current->getG() + distance(current, neighbor));
                    neighbor->setF(neighbor->getG() + neighbor->getH());
                    neighbor->setPrevious(current);
                    if (isNodeOnList(neighbor, open_list))
                    {
                        int place = findPlace(neighbor, open_list);
                        if (neighbor->getF() < open_list[place]->getF())
                        {
                            open_list[place] = neighbor;
                        }
                    }
                    else
                    {
                        open_list.push_back(neighbor);
                    }
                }
            }
        }
        current = findLowestCostNode(open_list);
        if (current == nullptr)
        {
            return {};
        }
        closed_list.push_back(current);
        int place = findPlace(current, open_list);
        open_list.erase(open_list.begin() + place);
    }
    searchPath();
    return path;
}

nodeList Astar::findNeighbor(Node *n)
{
    nodeList neighbor;
    int x = n->getX();
    int y = n->getY();
    if (x > 0)
    {
        neighbor.push_back(map->nodeAt(x - 1, y));
    }
    if (x < map->getWidth() - 1)
    {
        neighbor.push_back(map->nodeAt(x + 1, y));
    }
    if (y > 0)
    {
        neighbor.push_back(map->nodeAt(x, y - 1));
    }
    if (y < map->getHeight() - 1)
    {
        neighbor.push_back(map->nodeAt(x, y + 1));
    }
    if (x > 0 && y > 0)
    {
        neighbor.push_back(map->nodeAt(x - 1, y - 1));
    }
    if (x > 0 && y < map->getHeight() - 1)
    {
        neighbor.push_back(map->nodeAt(x - 1, y + 1));
    }
    if (x < map->getWidth() - 1 && y > 0)
    {
        neighbor.push_back(map->nodeAt(x + 1, y - 1));
    }
    if (x < map->getWidth() - 1 && y < map->getHeight() - 1)
    {
        neighbor.push_back(map->nodeAt(x + 1, y + 1));
    }
    for (size_t i = 0; i < neighbor.size(); i++)
    {
        if (neighbor[i]->getVal() != 0)
        {
            neighbor.erase(neighbor.begin() + i);
            i--;
        }
    }
    return neighbor;
}

bool Astar::isNodeOnList(Node *n, const nodeList &nlist)
{
    for (Node *node : nlist)
    {
        if (node->getX() == n->getX() && node->getY() == n->getY())
        {
            return true;
        }
    }
    return false;
}

int Astar::findPlace(Node *n, const nodeList &nlist)
{
    for (size_t i = 0; i < nlist.size(); i++)
    {
        if (nlist[i] == n)
        {
            return i;
        }
    }
    return -1;
}

Node *Astar::findLowestCostNode(const nodeList &nlist)
{
    Node *lowestCostNode = nullptr;
    int lowestCost = -1;
    for (Node *node : nlist)
    {
        if (node->getF() < lowestCost || lowestCost == -1)
        {
            lowestCost = node->getF();
            lowestCostNode = node;
        }
    }
    return lowestCostNode;
}

void Astar::printPath(Table &map, nodeList *path, nodeList *openList, nodeList *closedList)
{
    std::ofstream file;
    file.open("map.ppm");
    file << "P3\n"
         << map.getHeight() << " " << map.getWidth() << "\n255\n";
    for (int i = 0; i < map.getHeight(); i++)
    {
        for (int j = 0; j < map.getWidth(); j++)
        {
            if (isNodeOnList(map.nodeAt(j, i), *path))
            {
                file << "255 0 0 ";
            }
            else if (isNodeOnList(map.nodeAt(j, i), *openList))
            {
                file << "0 0 255 ";
                map.nodeAt(j, i)->setVal(6);
            }
            else if (isNodeOnList(map.nodeAt(j, i), *closedList))
            {
                file << "0 255 0 ";
                map.nodeAt(j, i)->setVal(7);
            }
            else if (map.nodeAt(j, i)->getVal() != 0)
            {
                file << "0 0 0\n";
            }
            else
            {
                file << "255 255 255\n";
            }
        }
    }
    file.close();
}

nodeList *Astar::getOpen()
{
    return &open_list;
}

nodeList *Astar::getClosed()
{
    return &closed_list;
}

void Astar::printList(nodeList l)
{
    for (Node *n : l)
    {
        printf("x : %i, y : %i\n", n->getX(), n->getY());
    }
    printf("\n");
}