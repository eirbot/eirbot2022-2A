class Sample{
    int x;
    int y;
    // 0 : rouge
    // 1 : vert
    // 2 : bleu
    int color;
    public:
    Sample(int,int,int);
    void setPosition(int, int);
    int getX() const;
    int getY() const;
    int getColor() const;
};