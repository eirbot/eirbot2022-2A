#include <vector>

class Node{
    int val;
    int x;
    int y;
    float f = 0;
    float g = 0;
    float h = 0;
    /* angle dans lequel le robot arrive sur le noeud*/
    int direction = 0;
    Node* previous = nullptr;
    public:
    /*ajout operator= et constructeur par recopie*/

    /**
     * @brief constructeur de la classe Node
     * @param x : abscisse du noeud
     * @param y : ordonnée du noeud
     * @param val : valeur du noeud
     */
    Node(int, int, int);
    ~Node();

    /**
     * @brief permet de modifier le cout G
     * @param g : cout G
     * 
     */
    void setG(float);

    /**
     * @brief permet de modifier le cout H
     * @param h : cout H
     * 
     */
    void setH(float);

    /**
     * @brief permet de modifier le cout F
     * @param f : cout F
     * 
     */
    void setF(float);

    /**
     * @brief permet de modifier l'attribut val
     * @param val : valeur du noeud
     * 
     */
    void setVal(int);

    /**
     * @brief permet de modifier l'attribut direction
     * @param dir : direction 
     * 
     */
    void setDir(int);

    /**
     * @brief permet de modifier le noeud précédent
     * @param n : noeud précédent 
     */
    void setPrevious(Node*);

    /**
     * @brief permet de récupérer le cout F
     */
    float getF() const;

    /**
     * @brief permet de récupérer le cout G
     */
    float getG() const;

    /**
     * @brief permet de récupérer le cout H
     */
    float getH() const;

    /**
     * @brief permet de récupérer l'attribut val
     */
    int getVal() const;

    /**
     * @brief permet de récupérer l'attribut direction
     */
    int getDir() const;

    /**
     * @brief permet de récupérer l'attribut x
     */
    int getX() const;

    /**
     * @brief permet de récupérer l'attribut y
     */
    int getY() const;

    /**
     * @brief permet de récupérer l'attribut previous
     */
    Node* getPrevious() const;
};