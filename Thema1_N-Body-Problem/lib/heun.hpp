#ifndef VELOCITY_VERLET_HPP
#define VELOCITY_VERLET_HPP

#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "heun.cpp"
using namespace std;


// declare the functions here
vector<vector<double>> heun(vector<vector<double>> table, double delta_t, int nr_Particles);



#endif