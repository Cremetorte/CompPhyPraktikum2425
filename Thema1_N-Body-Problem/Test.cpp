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
    
    //Test Velocity-Verlet with 2-body
    string file = "Input/3body.csv";
    vector<vector<double>> table = importData(file);

    vector<vector<double>> processed_data = process_data(table);

    cout << "Initial State: " << endl;
    print_data(processed_data);
    cout << endl;

    double t_max = 220;
    double eta = 0.001;
    double nr_steps = t_max/eta;
    
    cout << "Calculating " << nr_steps << " steps" << endl;
    
    for (int step = 0; step < nr_steps; step++){
        //cout << "step " << step << endl;
        vector<vector<double>> evolved_data = velocity_verlet(processed_data, eta, 3);
        //print_data(acceleration(evolved_data));

        //concatenate processed data and evolved data
        processed_data.insert(processed_data.end(), evolved_data.begin(),evolved_data.end());
        if (step % 10000 == 0) {
            cout << "step " << step << "/" << nr_steps << endl;
        }
    }

    //print_data(processed_data);

    cout << "Dimensions of Data:" << endl;
    print_Vector(dimensions(processed_data));


    string output_file = "Output/3-body/3Body_Velocity_Verlet.csv";
    write_to_csv(processed_data, output_file);
 

    return 0;
    
}