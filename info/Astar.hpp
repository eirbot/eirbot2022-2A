#include "Table.hpp"
#include <vector>
#include <iostream>
#include <fstream>

typedef std::vector<Node*> nodeList;

class Astar{
    Node *start;
    nodeList end;
    Table *map;
    public:
    nodeList open_list;
    nodeList closed_list;
    nodeList path;
    Astar(Node*, nodeList, Table* );
    ~Astar();
    float distance(Node *, Node *);
    void initialize();
    void searchPath();
    nodeList findPath();
    nodeList findNeighbor(Node*);
    static bool isNodeOnList(Node*, const nodeList&);
    static int findPlace(Node* , const nodeList&);
    static Node* findLowestCostNode(const nodeList&);
    void printPath(Table&, nodeList*, nodeList*, nodeList*);
    nodeList* getOpen();
    nodeList* getClosed();
    void printList(nodeList);
};