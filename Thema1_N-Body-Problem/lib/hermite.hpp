#ifndef HERMITE_HPP
#define HERMITE_HPP

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include "hermite.cpp"

using namespace std;


// declare the functions here
vector<vector<double>> hermite(vector<vector<double>> table, double delta_t, int nr_Particles);

#endif