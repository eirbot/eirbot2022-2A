#include "table.hpp"
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

void Table::lib()
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
void Table::fill()
{
    for (int i = 0; i < 1500; i++)
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

void Table::mouv()
{
    for (int i = 0; i < 6; i++)
    {
        for (int j = 0; j <= 60; j++)
        {
            for (int k = 0; k <= 70; k++)
            {
                table[palets[i][1] - k][palets[i][0] - j] = 2;
                table[palets[i][1] + k][palets[i][0] + j] = 2;
                table[palets[i][1] + k][palets[i][0] - j] = 2;
                table[palets[i][1] - k][palets[i][0] + j] = 2;
            }
        }
    }
    for (int j = 0; j <= 150; j++)
    {
        for (int k = 0; k <= 150; k++)
        {
            table[my_robot[1] - j][my_robot[0] - k] = 3;
            table[my_robot[1] + j][my_robot[0] + k] = 3;
            table[my_robot[1] - j][my_robot[0] + k] = 3;
            table[my_robot[1] + j][my_robot[0] - k] = 3;
        }
    }
    for (int j = 0; j <= 150; j++)
    {
        for (int k = 0; k <= 150; k++)
        {
            table[int(opp_robot[1] - j)][int(opp_robot[0] - k)] = 4;
            table[int(opp_robot[1] + j)][int(opp_robot[0] + k)] = 4;
            table[int(opp_robot[1] - j)][int(opp_robot[0] + k)] = 4;
            table[int(opp_robot[1] + j)][int(opp_robot[0] - k)] = 4;
        }
    }
}

void Table::show()
{
    fill();
    mouv();
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

void Table::set_palets(int x, int y, int pos)
{
    palets[pos][0] = x;
    palets[pos][1] = y;
}

void Table::set_my_robot(int x, int y)
{
    my_robot[0] = x;
    my_robot[1] = y;
}

void Table::set_opp_robot(int x, int y)
{
    opp_robot[0] = x;
    opp_robot[1] = y;
}

int main()
{
    Table t(30, 2000, 3000);
    t.show();
    t.set_my_robot(300, 1500);
    t.set_opp_robot(2750, 600);
    t.set_palets(890, 450, 0);
    t.show();
    return 0;
}