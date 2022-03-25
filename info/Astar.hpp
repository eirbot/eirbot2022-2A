#ifndef ASTAR_HPP
#define ASTAR_HPP

#include "Table.hpp"
#include <vector>
#include <iostream>
#include <fstream>

typedef std::vector<Node*> nodeList;

class Astar{
    Node *start;
    nodeList * end;
    Table *map;
    int direction;
    public:
    nodeList open_list;
    nodeList closed_list;
    nodeList path;
    Astar(Node *, nodeList *, Table *, int );
    ~Astar();
    static float distance(Node *, Node *);
    static float minDist(Node *, nodeList &);
    void searchPath();
    nodeList findPath();
    nodeList findNeighbor(Node*);
    static bool isNodeOnList(Node*, const nodeList&);
    static int findPlace(Node* , const nodeList&);
    static Node* findLowestCostNode(const nodeList&);
    void printPath(Table&, nodeList*, nodeList*, nodeList*);
    nodeList* getOpen();
    nodeList* getClosed();
    nodeList* getPath();
    void printList(nodeList);
};

#endif