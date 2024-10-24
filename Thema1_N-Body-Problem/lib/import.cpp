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