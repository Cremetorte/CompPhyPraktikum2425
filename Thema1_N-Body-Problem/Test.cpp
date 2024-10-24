#include "lib/functions.hpp"
#include <vector>
#include <iostream>

using namespace std;


int main() {
        
    vector<double> vector1 = {1, 2, 3};
    vector<double> vector2 = {4, 5, 6};
    vector<double> vectorsum;
    vectorsum = add_vectors(vector1, vector2);

    cout << "The sum of the vectors is: " << vectorsum[0] << ", " << vectorsum[1] << ", " << vectorsum[2] << endl;

    vector<double> vectordiff = subtract_vectors(vector1, vector2);
    cout << "The difference of the vectors is: " << vectordiff[0] << ", " << vectordiff[1] << ", " << vectordiff[2] << endl;

    vector<double> vectormult = scalar_multiplication(2, vector1);
    cout << "The scalar multiplication of the vector is: " << vectormult[0] << ", " << vectormult[1] << ", " << vectormult[2] << endl;
    
    double abs = absolute_value(vector1);
    cout << "The absolute value of the vector is: " << to_string(abs) << endl;
    return 0;

}