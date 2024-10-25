#include "lib/functions.hpp"
#include "lib/import.hpp"
#include <vector>
#include <iostream>

using namespace std;


int main() {
    //Test Vector functions  
    /* vector<double> vector1 = {1, 2, 3};
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
     */

    string file = "Input/100body.csv";
    vector<vector<double>> table = importData(file);
    vector<vector<double>> processed_data = process_data(table);

    cout << "Non-Processed-Data: " << endl;
    printData(table);
    cout << endl;

    cout << "Processed-Data: " << endl;
    printData(processed_data);
    cout << endl;

    cout << "COM before processing: ";
    print_Vector(calc_COM(table));
    cout << "COM after processing: ";
    print_Vector(calc_COM(processed_data));

    return 0;
    
}