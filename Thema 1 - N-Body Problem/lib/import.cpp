#include "import.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;


vector<vector<double>> importTable(const string& filename) {
    vector<vector<double>> table;
    ifstream file(filename);
    string line;

    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return table;
    }

    while (getline(file, line)) {
        vector<double> row;
        stringstream ss(line);
        string cell;
        while (getline(ss, cell, '\t')) {
            row.push_back(stod(cell));
        }
        table.push_back(row);
    }

    file.close();
    return table;
}