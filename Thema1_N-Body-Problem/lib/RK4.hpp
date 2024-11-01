#ifndef HEUN_HPP
#define HEUN_HPP

#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "RK4.cpp"
using namespace std;


// declare the functions here
vector<vector<double>> RK4(vector<vector<double>> table, double delta_t, int nr_Particles);



#endif