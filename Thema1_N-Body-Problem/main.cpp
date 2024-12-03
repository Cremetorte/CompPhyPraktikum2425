#include <iostream>
#include <string>
#include <sstream>
#include <cstdlib>
#include <functional>
#include "lib/import.hpp"
#include "lib/export.hpp"
#include "lib/euler.hpp"
#include "lib/euler-cromer.hpp"
#include "lib/hermite.hpp"
#include "lib/heun.hpp"
#include "lib/RK4.hpp"
#include "lib/velocity-verlet.hpp"
using namespace std;

int main(int argc, char* argv[]) {
    
    if (argc != 6) {
        cout << "Wrong number of arguments! Usage: " << argv[0] << " integrator N delta_t t_max video?" << endl;
        return -1;
    }

    function<vector<vector<double>>(vector<vector<double>> table, double delta_t, int nr_Particles)> integrator;

    //get Integrator
    if (string(argv[1]) == "euler") {
        integrator = euler;
    }
    else if (string(argv[1]) == "euler-cromer")
    {
        integrator = euler_cromer;
    }
    else if (string(argv[1]) == "hermite")
    {
        integrator = hermite;
    }
    else if (string(argv[1]) == "hermite")
    {
        integrator = hermite;
    }
    else if (string(argv[1]) == "heun")
    {
        integrator = heun;
    }
    else if (string(argv[1]) == "RK4")
    {
        integrator = RK4_field;
    }
    else if (string(argv[1]) == "velocity_verlet")
    {
        integrator = velocity_verlet;
    }
    else {
        cout << "Integrator has to be one of the following:" << endl;
        cout << "euler\neuler-cromer\nvelocity_verlet\nhermite\nhermite-it\nheun\nRK4" << endl; 
        return -1;
    }
    
    int N = stoi(argv[2]);
    double delta_t = stod(argv[3]);
    double t_max = stod(argv[4]);
    double nr_steps = t_max/delta_t;

    bool video = (string(argv[5]) == "true");
        
    

    stringstream inputfile_ss;
    inputfile_ss << "Input/" << N << "body.csv";
    string inputfile = inputfile_ss.str();
    stringstream outputfile_ss;
    outputfile_ss << "Output/" << N << "-body/" << N << "Body_" << string(argv[1]) << "_" << delta_t << ".csv";
    string outputfile = outputfile_ss.str();


    //import data
    vector<vector<double>> table = importData(inputfile);
    //process_data
    vector<vector<double>> processed_data = process_data(table);

    

    cout << "Beginning calculation" << endl;

    vector<vector<double>> evolved_data = integrator(processed_data, delta_t, N);
    processed_data.insert(processed_data.end(), evolved_data.begin(),evolved_data.end());
    
    for (int step = 1; step < nr_steps; step++){
        //output every 10th step:
        if (step%10 == 0) {
            cout << "\r" << "calculating step " << step << "/" << nr_steps << flush;
        }

        evolved_data = integrator(evolved_data, delta_t, N);

        //concatenate processed data and evolved data
        processed_data.insert(processed_data.end(), evolved_data.begin(),evolved_data.end());
        
        
    }
    cout << "\r" << "calculating step " << nr_steps << "/" << nr_steps << flush;
    cout << endl << "Finished calculation" << endl;

    //write to csv
    write_to_csv(processed_data, outputfile);

    if (video) {
        cout << endl << "Running python script VideoGenerator" << endl;

        stringstream outputfile_mp4_ss;
        outputfile_mp4_ss << "Output/" << N << "-body/" << N << "Body_" << string(argv[1]) << ".mp4";
        string outputfile_mp4 = outputfile_mp4_ss.str();

        stringstream command_ss;
        command_ss << "python3 Output/VideoGenerator.py " << outputfile << " " << N << " " << delta_t << " " << outputfile_mp4;
        string command = command_ss.str();
        int result = system(command.c_str());
        if (result != 0) {
            cerr << "Error: Command execution failed with status code " << result << endl;
            return result;
        }
    }



    
    return 0;
}