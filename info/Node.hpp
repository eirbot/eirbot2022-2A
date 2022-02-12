#include <vector>

class Node{
    int val;
    int x;
    int y;
    int f = 0;
    int g = 0;
    int h = 0;
    Node* previous = NULL;
    public:
    //ajout operator= et constructeur par recopie
    Node(int, int, int);
    ~Node();
    void setG(int);
    void setPrevious(Node*);
    int getF() const;
    int getG() const;
    int getVal() const;
    int getX() const;
    int getY() const;
    Node* getPrevious() const;
};