#include <iostream>
#include <vector>
#include <string>
#include "lib/import.hpp"
using namespace std;

int main() {
    //Dateiimport
    string file = "Input/100body.csv";
    vector<vector<double>> table = importData(file);
    vector<vector<double>> data = process_data(table);
    //printData(table);


    return 0;
}