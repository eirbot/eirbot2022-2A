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
            if (i < 10.2 && j > 117.5 && j < 132.5)
            {
                val = 1;
            }
            // coeff y = (300-149)/51 * x + 149
            if (j > ((200 - 149) / (51)) * i + 149)
            {
                val = 1;
            }
            if (j < 8 && i > 45 && i < 117)
            {
                val = 1;
            }
            if (j < 10 && i > 127.5 && i < 142.5)
            {
                val = 1;
            }
            // Palets
            if (j > 55.5 - 7.5 && j < 55.5 + 7.5 && i > 83 && i < 83 + 13)
            {
                val = 2;
            }
            if (j > 67.5 - 7.5 && j < 67.5 + 7.5 && i > 83 - 6.5 && i < 83 + 6.5)
            {
                val = 2;
            }
            if (j > 79.5 - 7.5 && j < 79.5 + 7.5 && i > 83 && i < 83 + 13)
            {
                val = 2;
            }
            // Palets zone fouille
            if (j > 128 - 7.5 && j < 128 + 7.5 && i > 81 && i < 81 + 13)
            {
                val = 2;
            }
            if (j > 132 - 7.5 && j < 132 + 7.5 && i > 100 && i < 100 + 13)
            {
                val = 2;
            }
            if (j > 147 - 7.5 && j < 147 + 7.5 && i > 90 && i < 90 + 13)
            {
                val = 2;
            }
            table[300 - i - 1][j - 1] = val;
            table[i][j] = val;
        }
    }
    for (int i = 0; i < 300; i++)
    {
        for (int j = 0; j < 200; j++)
        {
            int val = 0;
            // notre robot
            if (j > 70 - 15 && j < 70 + 15 && i < 30)
            {
                val = 3;
            }
            // Robot enemie
            if (i > 227 - 15 && i < 227 + 15 && j > 82 - 15 && j < 82 + 15)
            {
                val = 4;
            }
            if (val == 4 || val == 3)
            {
                table[i][j] = val;
            }
        }
    }
}
void Table::show()
{
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
            printf("%s%i ", s, val);
        }
        printf("\n");
    }
}

int main()
{
    Table t(3);
    t.fill();
    t.show();
    return 0;
}