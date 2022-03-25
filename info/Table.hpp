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
    robotList robots;
    sampleList samples;

    public:
    Table(int);
    ~Table();
    //voir s'il faut ajouter constructeur par recopie et operator=
    void fixeObstacle();
    void mouvObstacle();
    Node* nodeAt(int, int);
    int getScale();
    int getHeight();
    int getWidth();
    void show(int);
    void addRobot(Robot* );
    void addSample(Sample*);
};