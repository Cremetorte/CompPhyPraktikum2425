#include <iostream>
#include <vector>
#include <string>
#include "lib/import.hpp"
#include "lib/beschleunigung.hpp"
// #include "lib/functions.hpp"
using namespace std;

int main() {
    //Dateiimport
    string file = "Input/100body.csv";
    vector<vector<double>> table = importData(file);
    vector<vector<double>> data = process_data(table);
    print_data(table);
    cout << endl;
    print_data(acceleration(table));
    
    return 0;
}