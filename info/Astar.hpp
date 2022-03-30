#ifndef ASTAR_HPP
#define ASTAR_HPP

#include "Table.hpp"
#include <vector>
#include <iostream>
#include <fstream>

typedef std::vector<Node*> nodeList;

class Astar{
    Node *start;
    /* liste contenant l'ensemble des fin possible */ 
    nodeList * end;
    Table *map;
    int direction;
    nodeList open_list;
    nodeList closed_list;
    nodeList path;
    public:
    
    /**
     * @brief constructeur de la classe Astar
     * @param start : noeud de départ
     * @param end : liste contenant les noeuds de fin
     * @param map : table de la carte
     * @param direction : direction départ du robot
     */
    Astar(Node *, nodeList *, Table *, int );

    /**
     * @brief destructeur de la class Astar
     */
    ~Astar();

    /**
     * @brief permet de calculer la distance entre deux noeuds n1 et n2
     * @param n1 : noeud 1
     * @param n2 : noeud 2
     */
    static float distance(Node *, Node *);

    /**
     * @brief permet de trouver la distance la plus courte entre le noeud n1 et l'un des noeuds de la liste l
     * @param n1 : noeud
     * @param l : liste de noeuds
     */
    static float minDist(Node *, nodeList &);

    /**
     * @brief permet de stocker le chemin dans l'attribut path à partir de la liste de noeuds open_list
     */
    void searchPath();

    /**
     * @brief permet de trouver le chemin entre l'attribut start et l'attribut end
     * @param blocked true pour ne pas prendre en compte les palets comme obstacle, false sinon
     */
    nodeList findPath(bool = false);

    /**
     * @brief permet de trouver l'emsemble des voisins d'un noeud
     */
    nodeList findNeighbor(Node*,std::vector<int>);

    /**
     * @brief permet de savoir si le noeud n est dans la liste l
     * @param n : noeud
     * @param l : liste de noeuds
     */
    static bool isNodeOnList(Node*, const nodeList&);

    /**
     * @brief permet de savoir la place du noeud n dans la liste l
     * @param n : noeud
     * @param l : liste de noeuds
     */
    static int findPlace(Node* , const nodeList&);

    /**
     * @brief permet de trouver le noeud de la liste l ayant le cout le plus faible
     * @param l : liste de noeuds
     */
    static Node* findLowestCostNode(const nodeList&);

    /**
     * @brief permet de générer le fichier map.ppm permettant de visualiser le chemin
     * @param t : table
     * @param path : le chemin
     * @param open_list : liste des noeuds ouverts
     * @param closed_list : liste des noeuds fermés
     */
    void printPath(Table&, nodeList*, nodeList*, nodeList*);

    /** 
     * @brief permet d'accéder à l'attribut open_list
     **/    
    nodeList* getOpen();

    /** 
     * @brief permet d'accéder à l'attribut closed_list
     **/    
    nodeList* getClosed();


    /** 
     * @brief permet d'accéder à l'attribut path
     **/    
    nodeList* getPath();

    /**
     * @brief permet d'afficher une liste de noeuds
     * @param l : liste
     */
    void printList(nodeList);

    /**
     * @brief permet de savoir si la valeur du noeud n est dans la liste de valeur l
     * @param n : noeud
     * @param l : liste de valeur
     */
    bool valueIn(Node*, std::vector<int>);
};

#endif