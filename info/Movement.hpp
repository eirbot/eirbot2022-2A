#include "Astar.hpp"

class Movement{
    nodeList movDescription;
    int step = 1;
    float dist = 0;
    int angleR = 0;
    int angleA = 0;
    public:
    int oneStep();
    void importantPoints(nodeList);
    nodeList getMov();
};