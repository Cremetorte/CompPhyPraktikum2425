#include "import.hpp"
#include "functions.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;


/**
 * @brief Imports CSV Data to 2D-vector.
 * 
 * Every Row gets converted to a vector. These vectors are put into one vector.
 * The Entries should be in the following order:
 * x, y, z, v_x, v_y, v_z, mass
 * They have to be processed afterwards.
 * 
 * @param filename A string of the relative path of the file to be imported.
 * @return A 2D vector of doubles representing the non-processed data.
 */
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


/**
 * @brief Prints the entries in a 2d-Vector-Array to the console.
 * 
 * Prints the entries in a 2d-Vector-Array to the console for debugging/testing purposes.
 * 
 * @param data A 2D vector of doubles.
 * @return None.
 */
void print_data(vector<vector<double>> data) {
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
    double N = importedData.size();
    
    double total_mass = 0;

    //sum all masses
    for (vector<double> particle_i : importedData) {
        total_mass += particle_i[6];
    }

    //normalize all masses
    for (vector<double> &particle_i : importedData) {
        particle_i[6] /= total_mass;
    }

    //calculate COM
    vector<double> COM = calc_COM(importedData);



    //transform positions into COM
    for (int i = 0; i<3; i++){
        for (vector<double> &particle_i : importedData) {
            particle_i[i] -= COM[i];
            particle_i[i] = nearly_zero_to_zero(particle_i[i]);
        }
    }

    vector<double> COM_speed = {0,0,0};
    //calculate velocity of COM

    for (vector<double> particle_i : importedData) {
        vector<double> momentum = scalar_multiplication(particle_i[6],extract_velocity(particle_i));
        COM_speed = add_vectors(momentum, COM_speed);
        
    }

    //print_Vector(COM_speed);
    
    //transform velocities into COM Inertial frame
    for (int i = 3; i<6; i++){
        for (vector<double> &particle_i : importedData) {
            particle_i[i] -= COM_speed[i-3];
            particle_i[i] = nearly_zero_to_zero(particle_i[i]);
        }
    }
    

    return importedData;

}


