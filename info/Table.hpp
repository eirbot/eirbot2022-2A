#include <vector>
#include "Robot.hpp"
#include "Sample.hpp"

typedef std::vector<Robot*> robotList;
typedef std::vector<Sample*> sampleList;

class Table {
    int height;
    int width;
    int ** table;
    int scale;
    robotList robots;
    sampleList samples;
    //int palets[6][2] = {{900,555},{830,675},{900,795},{870,1270},{1050,1330},{950,1470}};
    //int my_robot[2] = {150,700};
    //int opp_robot[2] = {2850,700};

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