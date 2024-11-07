#include "lib/functions.hpp"
#include "lib/import.hpp"
#include "lib/export.hpp"
#include "lib/RK4.hpp"
#include <vector>
#include <iostream>
#include <string>
#include <fstream>

using namespace std;


int main() {
    
    string file = "Input/100body.csv";
    vector<vector<double>> table = importData(file);

    vector<vector<double>> processed_data = process_data(table);

    cout << "Initial State: " << endl;
    print_data(processed_data);
    cout << endl;

    double t_max = 2;
    double eta = 0.01;
    double nr_steps = t_max/eta;
    
    cout << "Calculating " << nr_steps << " steps" << endl;

    vector<vector<double>> evolved_data = RK4(processed_data, eta, 100);
    processed_data.insert(processed_data.end(), evolved_data.begin(),evolved_data.end());
    
    for (int step = 1; step < nr_steps; step++){
        //cout << "step " << step << endl;
        evolved_data = RK4(evolved_data, eta, 100);
        //print_data(acceleration(evolved_data));

        //concatenate processed data and evolved data
        processed_data.insert(processed_data.end(), evolved_data.begin(),evolved_data.end());
        if (0 == 0) {
            cout << "step " << step << "/" << nr_steps << endl;
        }
    }

    //print_data(processed_data);

    cout << "Dimensions of Data:" << endl;
    print_Vector(dimensions(processed_data));


    string output_file = "Output/2-body/1000Body_RK4.csv";
    write_to_csv(processed_data, output_file);
 

    return 0;
    
}