#ifndef HERMITE_iteriert_HPP
#define HERMITE_iteriert_HPP

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include "hermite_iteriert.cpp"

using namespace std;


// declare the functions here
vector<vector<double>> hermite_iteriert(vector<vector<double>> table, double delta_t, int nr_Particles);

#endif