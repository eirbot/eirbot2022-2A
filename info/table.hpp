class Table {
    int height;
    int width;
    int ** table;
    int scale;
    int palets[6][2] = {{900,555},{830,675},{900,795},{870,1270},{1050,1330},{950,1470}};
    int my_robot[2] = {150,700};
    int opp_robot[2] = {2850,700};

    public:
    Table(int, int, int);
    void lib();
    void fill();
    void mouv();
    void show();
    void set_palets(int, int, int);
    void set_my_robot(int, int);
    void set_opp_robot(int, int);
};