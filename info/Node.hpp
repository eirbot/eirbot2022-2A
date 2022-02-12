#include <vector>

class Node{
    int _val;
    int _x;
    int _y;
    int _f = 0;
    int _g = 0;
    int _h = 0;
    Node* _previous = NULL;
    public:
    //ajout operator= et constructeur par recopie
    Node(int, int, int);
    ~Node();
    void set_g(int);
    void set_previous(Node*);
    int get_f() const;
    int get_g() const;
    int get_val() const;
    int get_x() const;
    int get_y() const;
    Node* get_previous() const;
};