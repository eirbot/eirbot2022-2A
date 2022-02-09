class Arm {
    int position[6][2] = {{90,45},{30,70},{45,45},{30,60},{10,10},{40,80}};
    int x_arm;
    int y_arm;
    public:
    Arm(int, int);
    int move(int);
    int getX();
    int getY();
    void setX(int);
    void setY(int);
};