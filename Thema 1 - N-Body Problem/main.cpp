#include <iostream>
#include <vector>
#include <string>
#include "lib/import.hpp"
using namespace std;

int main() {
    string file = "Input/100body.csv";
    vector<vector<double>> table = importData(file);

    printData(table);


    return 0;
}