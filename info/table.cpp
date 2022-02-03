#include "table.hpp"
#include <cstdio>

Table::Table(int s)
{
    scale = s;
}

// vide : 0
// obstacle fixe : 1
// obstacle mobile : 2
// notre robot : 3
// robot enemie : 4
void Table::fill()
{
    for (int i = 0; i < 150; i++)
    {
        for (int j = 0; j < 200; j++)
        {
            int val = 0;
            // Gauche
            if (i <= 10 && j >= 117 && j <= 132)
            {
                val = 1;
            }
            // coeff y = (300-149)/51 * x + 149
            if (j >= ((200 - 149) / (51)) * i + 149)
            {
                val = 1;
            }
            if (j <= 8 && i >= 45 && i <= 117)
            {
                val = 1;
            }
            if (j <= 10 && i >= 127 && i <= 142)
            {
                val = 1;
            }
            table[300 - 1 - i][j] = val;
            table[i][j] = val;
        }
    }
}

void Table::mouv()
{
    for (int i = 0; i < 6; i++)
    {
        for (int j = 0; j <= 6; j ++)
        {
            for (int k = 0; k <= 7; k ++)
            {
                table[palets[i][0] - j][palets[i][1] - k] = 2;
                table[palets[i][0] + j][palets[i][1] + k] = 2;
                table[palets[i][0] - j][palets[i][1] + k] = 2;
                table[palets[i][0] + j][palets[i][1] - k] = 2;
            }
        }
    }
    for (int j = 0; j <= 15; j ++)
    {
        for (int k = 0; k <= 15; k ++)
        {
            table[my_robot[0] - j][my_robot[1] - k] = 3;
            table[my_robot[0] + j][my_robot[1] + k] = 3;
            table[my_robot[0] - j][my_robot[1] + k] = 3;
            table[my_robot[0] + j][my_robot[1] - k] = 3;
        }
    }
    for (int j = 0; j <= 15; j ++)
    {
        for (int k = 0; k <= 15; k ++)
        {
            table[int(opp_robot[0] - j)][int(opp_robot[1] - k)] = 4;
            table[int(opp_robot[0] + j)][int(opp_robot[1] + k)] = 4;
            table[int(opp_robot[0] - j)][int(opp_robot[1] + k)] = 4;
            table[int(opp_robot[0] + j)][int(opp_robot[1] - k)] = 4;
        }
    }
}

void Table::show()
{
    fill();
    mouv();
    for (int j = 0; j < 200; j += scale)
    {
        for (int i = 0; i < 300; i += scale)
        {
            const char *s = "";
            int val = table[i][j];
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
            printf("%s%i", s, val);
        }
        printf("\n");
    }
}

void Table::set_palets(int x, int y, int pos){
    palets[pos][0] = x;
    palets[pos][1] = y;
}

void Table::set_my_robot(int x, int y){
    my_robot[0] = x;
    my_robot[1] = y;
}

void Table::set_opp_robot(int x, int y){
    opp_robot[0] = x;
    opp_robot[1] = y;
}

int main()
{
    Table t(2);
    t.show();
    t.set_my_robot(30,150);
    t.set_opp_robot(275,60);
    t.set_palets(89,45,0);
    t.show();
    return 0;
}