#include "Table.hpp"
#include <cstdlib>
#include <cstdio>

Table::Table(int s, int h, int w)
{
    scale = s;
    height = h;
    width = w;
    map = (Node **)malloc(height * sizeof(Node *));
    for (int i = 0; i < height; i++)
    {
        map[i] = (Node *)malloc(width * sizeof(Node));
    }
}

Table::~Table()
{
    for (int i = 0; i < height; i++)
    {
        free(map[i]);
    }
    free(map);
}

// vide : 0
// obstacle fixe : 1
// obstacle mobile : 2
// notre robot : 3
// robot enemie : 4
void Table::fixeObstacle()
{
    for (int i = 0; i < width / 2; i++)
    {
        for (int j = 0; j < height; j++)
        {
            int val = 0;
            // Gauche
            if (i <= 102 && j >= 1175 && j <= 1325)
            {
                val = 1;
            }
            if (j >= ((height - 1490) / (510)) * i + 1490)
            {
                val = 1;
            }
            if (j <= 80 && i >= 450 && i <= 1170)
            {
                val = 1;
            }
            if (j <= 100 && i >= 1275 && i <= 1425)
            {
                val = 1;
            }

            Node n(val, width - 1 - i, j);
            map[j][width - 1 - i] = n;
            Node n1(val, i, j);
            map[j][i] = n1;
        }
    }
}

void Table::mouvObstacle()
{
    for (Sample *s : samples)
    {

        for (int j = 0; j <= 60; j++)
        {
            for (int k = 0; k <= 70; k++)
            {
                int val = 2;
                int y = s->getY() - k;
                int x = s->getX() - j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n(val, x, y);
                    map[y][x] = n;
                }
                y = s->getY() + k;
                x = s->getX() + j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n1(val, x, y);
                    map[y][x] = n1;
                }
                y = s->getY() + k;
                x = s->getX() - j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n2(val, x, y);
                    map[y][x] = n2;
                }
                y = s->getY() - k;
                x = s->getX() + j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n3(val, x, y);
                    map[y][x] = n3;
                }
            }
        }
    }
    for (Robot *r : robots)
    {
        for (int j = 0; j <= 150; j++)
        {
            for (int k = 0; k <= 150; k++)
            {
                int val;
                if (r->getTeam() == 0)
                {
                    val = 3;
                }
                else
                {
                    val = 4;
                }
                int y = r->getY() - k;
                int x = r->getX() - j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n(val, x, y);
                    map[y][x] = n;
                }
                y = r->getY() + k;
                x = r->getX() + j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n1(val, x, y);
                    map[y][x] = n1;
                }
                y = r->getY() + k;
                x = r->getX() - j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n2(val, x, y);
                    map[y][x] = n2;
                }
                y = r->getY() - k;
                x = r->getX() + j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n3(val, x, y);
                    map[y][x] = n3;
                }
            }
        }
    }
}

Node* Table::nodeAt(int x, int y){
    return &map[y][x];
}

int Table::getHeight(){
    return height;
}

int Table::getWidth(){
    return width;
}

void Table::show()
{
    fixeObstacle();
    mouvObstacle();
    for (int j = 0; j < height; j += scale)
    {
        for (int i = 0; i < width; i += scale)
        {
            const char *s = "";
            int val = map[j][i].getVal();
            if (val == 0)
            {
                s = "\x1B[34m";
            }
            if (val == 1)
            {
                s = "\x1B[32m";
            }
            if (val == 2)
            {
                s = "\x1B[33m";
            }
            if (val == 3)
            {
                s = "\x1B[0m";
            }
            if (val == 4)
            {
                s = "\x1B[31m";
            }
            printf("%s%i ", s, val);
        }
        printf("\n");
    }
}

void Table::addRobot(Robot *r)
{
    robots.push_back(r);
}

void Table::addSample(Sample *s)
{
    samples.push_back(s);
}

int main()
{
    Table t(30, 2000, 3000);
    Robot *r1 = new Robot(150, 700, 0);
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
    t.addSample(s6);
    t.show();
    delete (r1);
    delete (r2);
    delete (s1);
    delete (s2);
    delete (s3);
    delete (s4);
    delete (s5);
    delete (s6);
    return 0;
}