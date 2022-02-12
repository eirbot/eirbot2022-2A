#include "Table.hpp"
#include <cstdlib>
#include <cstdio>

Table::Table(int s, int h, int w)
{
    scale = s;
    height = h;
    width = w;
    table = (Node **)malloc(height * sizeof(Node *));
    for (int i = 0; i < height; i++)
    {
        table[i] = (Node *)malloc(width * sizeof(Node));
    }
}

Table::~Table()
{
    for (int i = 0; i < height; i++)
    {
        free(table[i]);
    }
    free(table);
}

// vide : 0
// obstacle fixe : 1
// obstacle mobile : 2
// notre robot : 3
// robot enemie : 4
void Table::fixe_obstacle()
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
            table[j][width - 1 - i] = n;
            Node n1(val, i, j);
            table[j][i] = n1;
        }
    }
}

void Table::mouv_obstacle()
{
    for (Sample *s : samples)
    {

        for (int j = 0; j <= 60; j++)
        {
            for (int k = 0; k <= 70; k++)
            {
                int val = 2;
                int y = s->get_y() - k;
                int x = s->get_x() - j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n(val, x, y);
                    table[y][x] = n;
                }
                y = s->get_y() + k;
                x = s->get_x() + j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n1(val, x, y);
                    table[y][x] = n1;
                }
                y = s->get_y() + k;
                x = s->get_x() - j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n2(val, x, y);
                    table[y][x] = n2;
                }
                y = s->get_y() - k;
                x = s->get_x() + j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n3(val, x, y);
                    table[y][x] = n3;
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
                if (r->get_team() == 0)
                {
                    val = 3;
                }
                else
                {
                    val = 4;
                }
                int y = r->get_y() - k;
                int x = r->get_x() - j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n(val, x, y);
                    table[y][x] = n;
                }
                y = r->get_y() + k;
                x = r->get_x() + j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n1(val, x, y);
                    table[y][x] = n1;
                }
                y = r->get_y() + k;
                x = r->get_x() - j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n2(val, x, y);
                    table[y][x] = n2;
                }
                y = r->get_y() - k;
                x = r->get_x() + j;
                if (y >= 0 && y < height && x >= 0 && x < width)
                {
                    Node n3(val, x, y);
                    table[y][x] = n3;
                }
            }
        }
    }
}

void Table::show()
{
    fixe_obstacle();
    mouv_obstacle();
    for (int j = 0; j < height; j += scale)
    {
        for (int i = 0; i < width; i += scale)
        {
            const char *s = "";
            int val = table[j][i].get_val();
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

void Table::add_robot(Robot *r)
{
    robots.push_back(r);
}

void Table::add_sample(Sample *s)
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
    t.add_robot(r1);
    t.add_robot(r2);
    t.add_sample(s1);
    t.add_sample(s2);
    t.add_sample(s3);
    t.add_sample(s4);
    t.add_sample(s5);
    t.add_sample(s6);
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