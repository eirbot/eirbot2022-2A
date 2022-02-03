class Table {
    int table[300][200];
    int scale;
    public:
    Table(int);
    void fill();
    void set(int, int , int ) const;
    int get(int , int );
    void show();
};