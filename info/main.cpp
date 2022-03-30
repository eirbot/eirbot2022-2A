#include "Movement.hpp"

#include <time.h> 

int main()
{
    float temps;
    clock_t t1;
    clock_t t2;

    t1 = clock();
    Table t(10);
    Robot *r2 = new Robot(284, 70, 1);
    Sample *s1 = new Sample(90, 55, 2);
    Sample *s2 = new Sample(83, 67, 2);
    Sample *s3 = new Sample(90, 79, 2);
    Sample *s4 = new Sample(87, 127, 2);
    Sample *s5 = new Sample(105, 133, 2);
    Sample *s6 = new Sample(95, 147, 2);
    t.addRobot(r2);
    t.addSample(s1);
    t.addSample(s2);
    t.addSample(s3);
    t.addSample(s4);
    t.addSample(s5);
    t.addSample(s6);
    t2 = clock();
    temps = (float)(t2-t1)/CLOCKS_PER_SEC;
    printf("%f\n", temps);
    t1 = clock();
    t.mouvObstacle();
    t2 = clock();
    temps = (float)(t2-t1)/CLOCKS_PER_SEC;
    printf("%f\n", temps);
    t1 = clock();
    Node *start = t.nodeAt(15, 15);
    Node *endNode = t.nodeAt(110, 80);
    Node *endNode2 = t.nodeAt(115, 95);
    //start->setPrevious(start);
    nodeList end;
    end.push_back(endNode);
    end.push_back(endNode2);
    Astar astar(start, &end, &t, 0);
    nodeList path = astar.findPath();
    //astar.printList(path);
    Movement mov;
    mov.importantPoints(path);
    t2 = clock();
    temps = (float)(t2-t1)/CLOCKS_PER_SEC;
    printf("%f\n", temps);
    //astar.printList(mov.getMov());
    int r = 0;
    while(r == 0)
    {
       r = mov.oneStep();
    }
    astar.printPath(t, &path, astar.getOpen(), astar.getClosed());
    Robot *r1 = new Robot(path.at(path.size() - 1)->getX(), path.at(path.size() - 1)->getY(), 0);
    t.addRobot(r1);
    t.mouvObstacle();
    t.show(3);
    delete (r1);
    delete (r2);
    delete (s1);
    delete (s2);
    delete (s3);
    delete (s4);
    delete (s5);
    delete (s6);
}
