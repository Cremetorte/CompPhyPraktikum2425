#include "lib/functions.hpp"
#include "lib/import.hpp"
#include "lib/export.hpp"
#include "lib/velocity-verlet.hpp"
#include <vector>
#include <iostream>
#include <string>
#include <fstream>

using namespace std;


int main() {
    //Test Vector functions  
    /* vector<double> vector1 = {1, 2, 3};
    vector<double> vector2 = {-4, 5, 6};
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

    //Test Processing of Data
/* 
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
 */


    //Test Velocity-Verlet with 2-body
    string file = "Input/2body.csv";
    vector<vector<double>> table = importData(file);
    cout << "Non-processed data: " << endl;
    print_data(table);
    cout << endl; 

    vector<vector<double>> processed_data = process_data(table);

    cout << "Initial State: " << endl;
    print_data(processed_data);
    cout << endl;

    double t_max = 2;
    double eta = 0.001;
    double nr_steps = t_max/eta;

    cout << "-------------------Calculation-------------------" << endl;
    for (int step = 0; step < 3; step++){
        cout << "step " << step << endl;
        vector<vector<double>> evolved_data = velocity_verlet(processed_data, eta, 2);
        print_data(acceleration(evolved_data));

        //concatenate processed data and evolved data
        processed_data.insert(processed_data.end(), evolved_data.begin(),evolved_data.end());
    }

    //print_data(processed_data);

    cout << "Dimensions of Data:" << endl;
    print_Vector(dimensions(processed_data));


    string output_file = "Output/2Body_Velocity_Verlet.csv";
    write_to_csv(processed_data, output_file);
 

    return 0;
    
}