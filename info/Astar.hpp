#include "Table.hpp"
#include <vector>
#include <iostream>
#include <fstream>

typedef std::vector<Node*> nodeList;

class Astar{
    std::ofstream file;
    Node* start;
    nodeList* end;
    Table map;
    public:
    nodeList open_list;
    nodeList closed_list;
    nodeList path;
    Astar(Node*, nodeList*, Table);
    int distance(Node *, Node *);
    void findPath();
    nodeList findNeighbor(Node*);
    static bool isNodeOnList(Node*, const nodeList&);
    static int findPlace(Node* , const nodeList&);
    static Node* findLowestCostNode(const nodeList&);
    void Astar::printPath(Table&, nodeList*, nodeList*, nodeList*)
};