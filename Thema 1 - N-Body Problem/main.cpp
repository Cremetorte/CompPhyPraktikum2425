#include <iostream>
#include <vector>
#include <string>
#include "lib/import.hpp"
using namespace std;

int main() {
    string file = "2body.dat";
    vector<vector<double>> table = importTable(file);

    cout << table[1][1];


    return 0;
}