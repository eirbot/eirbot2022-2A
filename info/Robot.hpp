class Robot{
    int _x;
    int _y;
    //0 : our team
    //1 : other team
    int _team;
    public:
    Robot(int,int,int);
    void set_position(int,int);
    int get_x() const;
    int get_y() const;
    int get_team() const;
};