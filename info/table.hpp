class Table {
    int table[300][200];
    int scale;
    int palets[6][2] = {{89,55},{83,67},{89,79},{87,127},{105,133},{95,147}};
    int my_robot[2] = {15,70};
    int opp_robot[2] = {285,70};
    public:
    Table(int);
    void fill();
    void mouv();
    void show();
    void set_palets(int, int, int);
    void set_my_robot(int, int);
    void set_opp_robot(int, int);
};