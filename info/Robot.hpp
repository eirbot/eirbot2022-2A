class Robot{
    int x;
    int y;
    //0 : our team
    //1 : other team
    int team;
    public:
    
    /**
     * @brief constructeur de la classe Robot
     * @param x : abscisse du robot
     * @param y : ordonnée du robot
     * @param team : équipe du robot
     */
    Robot(int,int,int);

    /**
     * @brief permet de modifier la position du robot
     * @param x
     * @param y
     */
    void setPosition(int,int);

    /**
     * @brief permet de récuperer l'abscisse du robot
     */
    int getX() const;

    /**
     * @brief permet de récuperer l'ordonnée du robot
     */
    int getY() const;

    /**
     * @brief permet de récuperer l'équipe du robot
     */
    int getTeam() const;
};