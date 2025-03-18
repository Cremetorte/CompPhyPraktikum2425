#include <vector>
#include <cmath>

class Electron {
public:
    double x;
    double y;
    double z;
    double phi;
    double theta;
    double T;

    // Constructor
    Electron(double x, double y, double z, double phi, double theta, double T) {
        this->x = x;
        this->y = y;
        this->z = z;
        this->phi = phi;
        this->theta = theta;
        this->T = T;
    }


    // --------------------------------------------------------------------------------- Methods
    bool isInside() {
        bool inX = (x >= -10) && (x <= 10);
        bool inY = (y >= -10) && (y <= 10);
        bool inZ = (z >= -10) && (z <= 10);
    }


};