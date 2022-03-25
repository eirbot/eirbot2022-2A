class Arm {
    char pos_nom[6][5] = {"INIT", "RESD", "PALP", "PALD", "STTP", "STTD"}; //cf differentes pos
    int position[6][2] = {{90,45},{30,70},{45,45},{30,60},{10,10},{40,80}};
    int x_arm;
    int y_arm;

    public:
    Arm(int, int); //classe bras
    int move(int); //deplacement du bras
    int set_pos(Arm, int); //definition de la nouvelle position
    
    //getters et setters
    int getX();
    int getY();
    void setX(int);
    void setY(int);
};