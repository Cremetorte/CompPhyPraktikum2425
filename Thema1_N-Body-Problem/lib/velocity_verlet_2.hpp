#ifndef VELOCITY_VERLET_2_HPP
#define VELOCITY_VERLET_2_HPP

#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "velocity_verlet_2.cpp"
using namespace std;


// declare the functions here
vector<vector<double>> velocity_verlet_V2(vector<vector<double>> table, double delta_t, int nr_Particles);



#endif