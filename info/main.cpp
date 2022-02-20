#include "Astar.hpp"

int main()
{
    Table t(30, 2000, 3000);
    /*Robot *r1 = new Robot(150, 700, 0);
    Robot *r2 = new Robot(2840, 700, 1);
    Sample *s1 = new Sample(900, 555, 2);
    Sample *s2 = new Sample(830, 675, 2);
    Sample *s3 = new Sample(900, 795, 2);
    Sample *s4 = new Sample(870, 1270, 2);
    Sample *s5 = new Sample(1050, 1330, 2);
    Sample *s6 = new Sample(950, 1470, 2);
    t.addRobot(r1);
    t.addRobot(r2);
    t.addSample(s1);
    t.addSample(s3);
    t.addSample(s4);
    t.addSample(s5);
    t.addSample(s6);*/
    Node *start = t.nodeAt(0, 0);
    Node *endNode = t.nodeAt(2999, 0);
    start->setPrevious(start);
    nodeList end;
    end.push_back(endNode);
    Astar astar(start, end, &t);
    nodeList path = astar.findPath();
    astar.printList(path);
    //astar.printPath(t,&path,astar.getOpen(), astar.getClosed());
    //t.show();
    /*delete (r1);
    delete (r2);
    delete (s1);
    delete (s2);
    delete (s3);
    delete (s4);
    delete (s5);
    delete (s6);*/
}
