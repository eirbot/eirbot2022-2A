class Sample{
    int x;
    int y;
    // 0 : rouge
    // 1 : vert
    // 2 : bleu
    int color;
    public:

    /**
     * @brief constructeur de la classe Sample
     * @param x : abscisse du sample
     * @param y : ordonnée du sample
     * @param color : couleur du sample
     */
    Sample(int,int,int);

    /**
     * @brief permet de modifer la position du palet
     */
    void setPosition(int, int);

    /**
     * @brief permet de recuperer l'abscisse du palet
     */
    int getX() const;

    /**
     * @brief permet de recuperer l'ordonnée du palet
     */
    int getY() const;

    /**
     * @brief permet de recuperer la couleur du palet
     */
    int getColor() const;
};