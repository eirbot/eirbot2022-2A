#include "Astar.hpp"

class Movement{
    nodeList movDescription;
    /* entier permettant de savoir si on a deja passer un noeud ou non */
    int pass = 0;
    /* étape actuelle*/
    int step = 1;
    float dist = 0;
    int angleR = 0;
    int angleA = 0;
    public:

    /**
        * @brief permet d'effectuer une étape du mouvement
        */
    int oneStep();

    /**
        * @brief permet de déterminer les endroits de la table pars où il doit passer
        */
    void importantPoints(nodeList);
    
    /**
        * @brief permet de récupérer l'attribute movDescription
        */
    nodeList getMov();
};