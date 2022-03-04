#include "Table.hpp"
#include <cstdlib>
#include <cstdio>
#include "math.h"


Table::Table(int s)
{
    scale = s;
    height = 2000 *scale/100;
    width = 3000*scale/100;
    map = (Node **)malloc(height * sizeof(Node *));
    for (int i = 0; i < height; i++)
    {
        map[i] = (Node *)malloc(width * sizeof(Node));
    }
    fixeObstacle();
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
            if (i <= int(102*scale/100) && j >= int(1175*scale/100) && j <= int(1325*scale/100))
            {
                val = 1;
            }
            if (j >= ((height - int(1490*scale/100)) / int(510*scale/100)) * i + int(1490*scale/100))
            {
                val = 1;
            }
            if (j <= int(80*scale/100) && i >= int(450*scale/100) && i <= int(1170*scale/100))
            {
                val = 1;
            }
            if (j <= int(100*scale/100) && i >= int(1275*scale/100) && i <= int(1425*scale/100))
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

        for (int j = 0; j <= int(60*scale/100); j++)
        {
            for (int k = 0; k <= int(70*scale/100); k++)
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
        for (int j = 0; j <= int(150*scale/100); j++)
        {
            for (int k = 0; k <= int(150*scale/100); k++)
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

int Table::getScale(){
    return scale;
}

void Table::show(int s)
{
    mouvObstacle();
    for (int j = 0; j < height; j += s)
    {
        for (int i = 0; i < width; i += s)
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
            printf("%s¤ ", s);
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
