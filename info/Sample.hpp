class Sample{
    int _x;
    int _y;
    // 0 : rouge
    // 1 : vert
    // 2 : bleu
    int _color;
    public:
    Sample(int,int,int);
    void set_position(int, int);
    int get_x() const;
    int get_y() const;
    int get_color() const;
};