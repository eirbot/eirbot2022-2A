#include "Table.hpp"
#include <cstdlib>
#include <cstdio>

Table::Table(int s, int h, int w)
{
    scale = s;
    height = h;
    width = w;
    table = (int **)malloc(height * sizeof(int *));
    for (int i = 0; i < height; i++)
    {
        table[i] = (int *)malloc(width * sizeof(int));
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
            table[j][width - 1 - i] = val;
            table[j][i] = val;
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
                table[s->get_y() - k][s->get_x() - j] = 2;
                table[s->get_y() + k][s->get_x() + j] = 2;
                table[s->get_y() + k][s->get_x() - j] = 2;
                table[s->get_y() - k][s->get_x() + j] = 2;
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
                table[r->get_y() - k][r->get_x() - j] = val;
                table[r->get_y() + k][r->get_x() + j] = val;
                table[r->get_y() + k][r->get_x() - j] = val;
                table[r->get_y() - k][r->get_x() + j] = val;
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
            int val = table[j][i];
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

void Table::add_robot(Robot *r){
    robots.push_back(r);
}

void Table::add_sample(Sample *s){
    samples.push_back(s);
}

int main()
{
    Table t(30, 2000, 3000);
    Robot * r1 = new Robot(150,700,0);
    Robot * r2 = new Robot(2850,700,1);
    Sample * s1 = new Sample(900,555,2);
    Sample * s2 = new Sample(830,675,2);
    Sample * s3 = new Sample(900,795,2);
    Sample * s4 = new Sample(870,1270,2);
    Sample * s5 = new Sample(1050,1330,2);
    Sample * s6 = new Sample(950,1470,2);
    t.add_robot(r1);
    t.add_robot(r2);
    t.add_sample(s1);
    t.add_sample(s2);
    t.add_sample(s3);
    t.add_sample(s4);
    t.add_sample(s5);
    t.add_sample(s6);
    t.show();
    return 0;
}