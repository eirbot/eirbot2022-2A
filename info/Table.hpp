#include <vector>
#include "Robot.hpp"
#include "Sample.hpp"
#include "Node.hpp"

typedef std::vector<Robot*> robotList;
typedef std::vector<Sample*> sampleList;

class Table {
    int height;
    int width;
    Node ** table;
    int scale;
    robotList robots;
    sampleList samples;

    public:
    Table(int, int, int);
    ~Table();
    //voir s'il faut ajouter constructeur par recopie et operator=
    void fixe_obstacle();
    void mouv_obstacle();
    void show();
    void add_robot(Robot* );
    void add_sample(Sample*);
};