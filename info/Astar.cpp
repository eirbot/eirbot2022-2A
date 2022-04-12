#include "Astar.hpp"
#include <string>
#include <math.h>
#include <bits/stdc++.h>

#define turnCost 0

Astar::Astar(Node *n, nodeList *nlist, Table *t, int d) : start(n), end(nlist), map(t), direction(d) {}

float Astar::distance(Node *n1, Node *n2)
{
    return sqrt((n2->getX() - n1->getX()) * (n2->getX() - n1->getX()) + (n2->getY() - n1->getY()) * (n2->getY() - n1->getY()));
}

Astar::~Astar() {}

float Astar::minDist(Node *n, nodeList &nlist)
{
    float lowestDist = -1;
    for (Node *end : nlist)
    {
        if (distance(n, end) < lowestDist || lowestDist == -1)
        {
            lowestDist = distance(n, end);
        }
    }
    return lowestDist;
}

void Astar::searchPath()
{
    Node *current = closed_list[closed_list.size() - 1];
    while (current != nullptr)
    {
        path.push_back(current);
        current = current->getPrevious();
    }
    std::reverse(path.begin(), path.end());
}

nodeList Astar::findPath(bool blocked)
{
    int tmpDir = 0;
    Node *current = start;
    current->setG(0);
    current->setH(0);
    current->setF(current->getG() + current->getH());
    current->setPrevious(nullptr);
    current->setDir(direction);
    open_list.push_back(current);
    closed_list.push_back(current);

    bool obs = false;
    std::vector<int> values;
    values.push_back(0);
    values.push_back(3);
    if (blocked)
    {
        values.push_back(2);
    }

    for (Node *n : *end)
    {
        if (valueIn(n, values))
        {
            obs = true;
        }
    }

    if (!obs)
    {
        searchPath();
        return path;
    }

    while (!isNodeOnList(current, *end))
    {
        nodeList neighbors = findNeighbor(current, values);
        for (Node *neighbor : neighbors)
        {
            if (neighbor != nullptr)
            {
                if (!isNodeOnList(neighbor, closed_list))
                {
                    if (neighbor->getY() - current->getY() == -1)
                    {
                        if (neighbor->getX() - current->getX() == -1)
                        {
                            tmpDir = 7;
                        }
                        if (neighbor->getX() - current->getX() == 1)
                        {
                            tmpDir = 1;
                        }
                        if (neighbor->getX() - current->getX() == 0)
                        {
                            tmpDir = 0;
                        }
                    }
                    if (neighbor->getY() - current->getY() == 1)
                    {
                        if (neighbor->getX() - current->getX() == -1)
                        {
                            tmpDir = 5;
                        }
                        if (neighbor->getX() - current->getX() == 1)
                        {
                            tmpDir = 3;
                        }
                        if (neighbor->getX() - current->getX() == 0)
                        {
                            tmpDir = 4;
                        }
                    }
                    if (neighbor->getY() - current->getY() == 0)
                    {
                        if (neighbor->getX() - current->getX() == -1)
                        {
                            tmpDir = 6;
                        }
                        if (neighbor->getX() - current->getX() == 1)
                        {
                            tmpDir = 2;
                        }
                    }
                    float tmpG = current->getG() + distance(current, neighbor);
                    if (direction != tmpDir)
                    {
                        if (current == start)
                        {
                            tmpG = tmpG;
                        }
                        else
                        {
                            tmpG = tmpG + turnCost;
                        }
                    }
                    if (isNodeOnList(neighbor, open_list))
                    {
                        int place = findPlace(neighbor, open_list);
                        if (tmpG <= open_list[place]->getG())
                        {
                            neighbor->setDir(tmpDir);
                            neighbor->setG(tmpG);
                            neighbor->setH(minDist(neighbor, *end));
                            neighbor->setF(neighbor->getG() + neighbor->getH());
                            neighbor->setPrevious(current);
                            open_list[place] = neighbor;
                        }
                    }
                    else
                    {
                        neighbor->setDir(tmpDir);
                        neighbor->setG(tmpG);
                        neighbor->setH(minDist(neighbor, *end));
                        neighbor->setF(neighbor->getG() + neighbor->getH());
                        neighbor->setPrevious(current);
                        open_list.push_back(neighbor);
                    }
                }
            }
        }
        current = findLowestCostNode(open_list);
        if (current == nullptr || open_list.empty())
        {
            return path;
        }
        direction = current->getDir();
        closed_list.push_back(current);
        int place = findPlace(current, open_list);
        open_list.erase(open_list.begin() + place);
    }
    searchPath();
    return path;
}

nodeList Astar::findNeighbor(Node *n, std::vector<int> values)
{
    nodeList neighbor;
    int x = n->getX();
    int y = n->getY();
    int scale = map->getScale();
    bool right = true;
    bool left = true;
    bool up = true;
    bool down = true;
    for (int i = -150 * scale / 100; i <= 150 * scale / 100; i++)
    {
        if (x > 150 * scale / 100)
        {
            if (!valueIn(map->nodeAt(x - 150 * scale / 100 - 1, y + i), values))
            {
                left = false;
            }
        }
        if (x < map->getWidth() - 150 * scale / 100 - 1)
        {
            if (!valueIn(map->nodeAt(x + 150 * scale / 100 + 1, y + i), values))
            {
                right = false;
            }
        }
        if (y > 150 * scale / 100)
        {
            if (!valueIn(map->nodeAt(x + i, y - 150 * scale / 100 - 1), values))
            {
                up = false;
            }
        }
        if (y < map->getHeight() - 150 * scale / 100 - 1)
        {
            if (!valueIn(map->nodeAt(x + i, y + 150 * scale / 100 + 1), values))
            {
                down = false;
            }
        }
    }
    left = left && x > 150 * scale / 100;
    right = right && x < map->getWidth() - 150 * scale / 100 - 1;
    up = up && y > 150 * scale / 100;
    down = down && y < map->getHeight() - 150 * scale / 100 - 1;

    if (left)
    {
        neighbor.push_back(map->nodeAt(x - 1, y));
    }
    if (right)
    {
        neighbor.push_back(map->nodeAt(x + 1, y));
    }
    if (up)
    {
        neighbor.push_back(map->nodeAt(x, y - 1));
    }
    if (down)
    {
        neighbor.push_back(map->nodeAt(x, y + 1));
    }
    if (left && up)
    {
        neighbor.push_back(map->nodeAt(x - 1, y - 1));
    }
    if (left && down)
    {
        neighbor.push_back(map->nodeAt(x - 1, y + 1));
    }
    if (right && up)
    {
        neighbor.push_back(map->nodeAt(x + 1, y - 1));
    }
    if (right && down)
    {
        neighbor.push_back(map->nodeAt(x + 1, y + 1));
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
    float lowestCost = -1;
    for (Node *node : nlist)
    {
        if (node->getF() <= lowestCost || lowestCost == -1)
        {
            if (node->getF() < lowestCost || lowestCost == -1)
            {
                lowestCost = node->getF();
                lowestCostNode = node;
            }
            else
            {
                if (node->getG() < lowestCostNode->getG())
                {
                    lowestCost = node->getF();
                    lowestCostNode = node;
                }
            }
        }
    }
    return lowestCostNode;
}

void Astar::printPath(Table &map, nodeList *path, nodeList *openList, nodeList *closedList)
{
    std::ofstream file;
    file.open("map.ppm");
    file << "P3\n"
         << map.getWidth() << " " << map.getHeight() << "\n255\n";
    for (int i = 0; i < map.getHeight(); i++)
    {
        for (int j = 0; j < map.getWidth(); j++)
        {
            if (isNodeOnList(map.nodeAt(j, i), *path))
            {
                file << "0 255 0 ";
            }
            else if (isNodeOnList(map.nodeAt(j, i), *openList))
            {
                file << "0 200 255 ";
            }
            else if (isNodeOnList(map.nodeAt(j, i), *closedList))
            {
                file << "150 0 255 ";
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

nodeList *Astar::getPath()
{
    return &path;
}

void Astar::printList(nodeList l)
{
    for (Node *n : l)
    {
        printf("x : %i, y : %i, angle : %i, g : %f, h : %f\n", n->getX(), n->getY(), n->getDir(), n->getG(), n->getH());
    }
    printf("\n");
}

bool Astar::valueIn(Node *n, std::vector<int> values)
{
    bool b = false;
    for (size_t i = 0; i < values.size(); i++)
    {
        if (n->getVal() == values.at(i))
        {
            b = true;
        }
    }
    return b;
}