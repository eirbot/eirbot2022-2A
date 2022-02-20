#include <vector>

class Node{
    int val;
    int x;
    int y;
    float f = 0;
    float g = 0;
    float h = 0;
    Node* previous = nullptr;
    public:
    //ajout operator= et constructeur par recopie
    Node(int, int, int);
    ~Node();
    void setG(float);
    void setH(float);
    void setF(float);
    void setVal(int);
    void setPrevious(Node*);
    float getF() const;
    float getG() const;
    float getH() const;
    int getVal() const;
    int getX() const;
    int getY() const;
    Node* getPrevious() const;
};