/*
GCMC Simulation eines 2d Gittermodells harter Stäbchen. 

Benutzung: ./gcmc Z
Z: double, Ordnungsparameter

Output:
- Output/observations_Z=xxxx.csv: CSV-Datei mit Observablen
*/

#include <vector>
#include <iostream>
#include <cmath>
#include <chrono>
#include <iomanip>
#include <sstream>
#include "lib/randGen.hpp"
#include "lib/thermo.hpp"
#include "lib/ImExport.hpp"

using namespace std;

const int latPoints = 64;
long int total_it = 4 * pow(10, 9);

bool OUTPUT = true;

int main(int argc, char* argv[]) {
    // ------------------------------------------------------------------------------------ Parse Arguments
    if (!(argc == 2 || argc == 3)) {
        cout << "Wrong number of arguments! Usage: " << argv[0] << " Z [output]" << endl;
        return -1;
    }
    double Z = stod(argv[1]);

    if (string(argv[2]) == "false") {
        OUTPUT = false;
    }

    // ------------------------------------------------------------------------------------ Begin Calculation

    cout << "Beginning calculation for z=" << Z << ", doing " << total_it << " iterations." << endl;

    // starting time for commandline output
    auto start = chrono::high_resolution_clock::now();

    // initialize Quantities
    vector<vector<int>> horizontalRods;
    vector<vector<int>> verticalRods;
    int occupationField[latPoints][latPoints] = {0};
    vector<vector<double>> observations;

    // thermalize
    for (int i=0; i<1000; i++) {
        gcmcStep(horizontalRods, verticalRods, occupationField, Z);
    }


    bool savedOnePhase = false;
    bool savedTwoPhase = false;

    // Start GCMC steps
    for (long int t = 1; t < total_it; t++) {
        gcmcStep(horizontalRods, verticalRods, occupationField, Z);
        
        if (t % 1000 == 0) { // calculate observables
            observations.push_back(observables(horizontalRods, verticalRods, occupationField));
            // if (observations.back()[4] == 1 && !savedOnePhase) {
            //     string filenamehor = "Output/horizontal_twoPhase_z=" + to_string(Z) + ".csv";
            //     string filenamever = "Output/vertical_twoPhase_z=" + to_string(Z) + ".csv";
            //     exportMatrixToCSV(horizontalRods, filenamehor);
            //     exportMatrixToCSV(verticalRods, filenamever);
            //     savedOnePhase = true;
            // }
            // if (observations.back()[4] == 0 && !savedTwoPhase) {
            //     string filenamehor = "Output/horizontal_onePhase_z=" + to_string(Z) + ".csv";
            //     string filenamever = "Output/vertical_onePhase_z=" + to_string(Z) + ".csv";
            //     exportMatrixToCSV(horizontalRods, filenamehor);
            //     exportMatrixToCSV(verticalRods, filenamever);
            //     savedTwoPhase = true;
            // }
        }
        if (t % 1000000 == 0 && OUTPUT) { // calculate elapsed time, estimate total time
            auto ittime = chrono::high_resolution_clock::now();
            auto duration = chrono::duration_cast<chrono::seconds>(ittime - start);

            int el_minutes = duration.count() / 60; // get minutes
            int el_seconds = duration.count() % 60; // get seconds

            long int est_time = static_cast<long int>(duration.count()) * total_it / t;

            int est_minutes = est_time / 60; // get minutes
            int est_seconds = est_time % 60; // get seconds

            // Add time to output stream
            cout << "\rCalculated " << fixed << setprecision(2) << setw(5) << (double)t / total_it * 100.0 << "% of all steps. ";
            cout << "Elapsed/Estimated time [min:s]: " << el_minutes << ":" << setw(2) << setfill('0') << el_seconds;
            cout << "/" << est_minutes << ":" << setw(2) << setfill('0') << setprecision(2) << est_seconds << "      ";
        }
    }
    cout << "\nfinished calculation" << endl;

    // ---------------------------------------------------------------------------- Export observables
    stringstream filename_ss;
    filename_ss.str("");
    filename_ss << "Output/obs_z=" << setw(5) << setfill('0') << setprecision(2) << Z << ".csv";
    string filename = filename_ss.str();

    exportObservablesToCSV(observations, filename);


    

    // print2dArray(occupationField);


    return 1;
}