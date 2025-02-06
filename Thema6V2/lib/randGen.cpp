#include <random>
#include "randGen.hpp"

using namespace std;

// initialize random generators for future use
random_device rd;  
mt19937 gen(rd());


/**
 * @brief Generates a random integer inside the given bounds.
 * 
 * Bounds are included: randomInt(min, max) is an element of [min, max] 
 * 
 * @param lower_bound Lower bound of the random integer
 * @param upper_bound Upper bound of the random integer
 */
int randomInt(int lower_bound, int upper_bound) {
    uniform_int_distribution<> dis(lower_bound, upper_bound);

    int res = dis(gen);

    return res;
}


/**
 * @brief Generates a random double inside the given bounds.
 * 
 * Bounds are included: randomDouble(min, max) is an element of [min, max] 
 * 
 * @param lower_bound Lower bound of the random double
 * @param upper_bound Upper bound of the random double
 */
double randomDouble(double lower_bound, double upper_bound) { 
    uniform_real_distribution<> dis(lower_bound, upper_bound);

    double res = dis(gen);

    return res;
}

