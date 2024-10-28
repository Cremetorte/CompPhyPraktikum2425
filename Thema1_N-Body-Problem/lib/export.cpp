#include "import.hpp"
#include "functions.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;


/**
 * @brief Exports data 2d-Vector to CSV file.
 * 
 * Exports data 2d-Vector to CSV file with arbitrary delimiter.
 * 
 * @param data vector<vector<double>>, values become values of CSV.
 * @param path_filename relative path and filename of the file to be generated.
 * 
 * @return None.
 */
void write_to_csv(vector<vector<double>> data,const string& path_filename) {
    cout << "\nAttemtring to write to " << path_filename << "..." << endl;
    ofstream outputFile(path_filename);

    if (!outputFile.is_open()) {
        cerr << "Error: Could not open file " << path_filename << endl;
        return;
    }

    stringstream line;
    for (vector<double> row : data) {
        line.str("");
        for (int i = 0; i < row.size()-1; i++) {
            line << row[i];
            line << ",";
        }
        line << row[row.size()-1] << "\n";
        outputFile << line.str();
    }

    outputFile.close();

}