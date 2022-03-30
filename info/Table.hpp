#include <vector>
#include "Robot.hpp"
#include "Sample.hpp"
#include "Node.hpp"

typedef std::vector<Robot*> robotList;
typedef std::vector<Sample*> sampleList;

class Table {
    int height;
    int width;
    Node ** map;
    int scale;
    /*liste des robot sur la table*/
    robotList robots;
    /*liste des palets sur la table*/
    sampleList samples;

    public:
    /**
     * @brief constructeur de la classe Table
     * @param scale : échelle de la table
     */
    Table(int);

    /**
     * @brief destructeur de la classe Table
     */
    ~Table();
    //voir s'il faut ajouter constructeur par recopie et operator=

    /**
     * @brief permet positionner les obstacle fix sur la table
     */
    void fixeObstacle();

    /**
     * @brief permet de positionner les robots et les palets sur la table
     */
    void mouvObstacle();

    /**
     * @brief permet de connaitre le noeud se trouvant a la position x,y
     * @param x : abscisse
     * @param y : ordonnée
     */
    Node* nodeAt(int, int);

    /**
     * @brief permet d'optenir l'échelle de la table (précision)
     * 
     */
    int getScale();

    /**
     * @brief permet d'optenir la largeur de la table
     * 
     */
    int getHeight();

    /**
     * @brief permet d'optenir la longueur de la table
     * 
     */
    int getWidth();

    /**
     * @brief permet d'afficher la table dans le terminale
     * @param scale : échelle d'affichage (affichage 1 noeud sur scale)
      */
    void show(int);

    /**
     * @brief permet d'ajouter un robot dans la liste robotlist
     * @param robot : robot à ajouter
     */
    void addRobot(Robot* );

    /**
     * @brief permet d'ajouter un palet dans la liste samplelist
     * @param sample : palet à ajouter
     */
    void addSample(Sample*);
};