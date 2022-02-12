class Robot{
    int x;
    int y;
    //0 : our team
    //1 : other team
    int team;
    public:
    Robot(int,int,int);
    void setPosition(int,int);
    int getX() const;
    int getY() const;
    int getTeam() const;
};