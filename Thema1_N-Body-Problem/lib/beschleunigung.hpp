#ifndef BESCHLEUNIGUNG_HPP
#define BESCHLEUNIGUNG_HPP

#include <iostream>
#include <vector>
#include <string>
#include "beschleunigung.cpp"
using namespace std;


// declare the functions here
vector<vector<double>> acceleration(vector<vector<double>> table);
vector<vector<double>> acceleration_parallel(const vector<vector<double>>& table);
function<vector<double>(const int&, const vector<double>&)> acceleration_field_particle_i(const vector<vector<double>>& table);

#endif