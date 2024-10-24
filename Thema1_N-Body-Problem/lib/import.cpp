#include "import.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;


vector<vector<double>> importData(const string& filename) {
    vector<vector<double>> data;
    ifstream file(filename);
    string line;

    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return data;
    }

    while (getline(file, line)) {
        vector<double> row;
        stringstream ss(line);
        string value;

        while (getline(ss, value, ',')) {
            row.push_back(stod(value));
        }
        data.push_back(row);
       
    }

    file.close();
    return data;
}

void printData(vector<vector<double>> data) {
    for (const auto& row : data) {
        for (const auto& value : row) {
            cout << value << ",";
        }
        cout << endl;
    }
}

/**
 * @brief Converts data to COM system and normalizes masses.
 * 
 * Makes sure the center of mass does not shift. Also, the sum of all masses sum up to 1.
 * 
 * @param importedData A 2D vector of doubles representing the imported data.
 * @return A 2D vector of doubles representing the processed data.
 */
vector<vector<double>> process_data(vector<vector<double>> importedData) {
    int N = importedData.size();
    
    double total_mass = 0;

    //sum all masses
    for (vector<double> particle_i : importedData) {
        total_mass += particle_i[6];
    }

    //normalize all masses
    for (vector<double> particle_i : importedData) {
        particle_i[6] /= total_mass;
    }

    
    vector<double> COM = ;

    //calculate COM
    for (int i = 0; i<3; i++){
        for (vector<double> particle_i : importedData) {
            COM[i] += particle_i[i]*particle_i[6];
        }
    }

    //transform into COM
    for (int i = 0; i<3; i++){
        for (vector<double> particle_i : importedData) {
            COM[i] += particle_i[i]*particle_i[6];
        }
    }


    return importedData;

}