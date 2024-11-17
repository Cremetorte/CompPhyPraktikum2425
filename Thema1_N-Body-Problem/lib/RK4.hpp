#ifndef RK4_HPP
#define RK4_HPP

#include <vector>
#include <functional>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "RK4.cpp"
using namespace std;


// declare the functions here
vector<vector<double>> RK4(const vector<vector<double>>& table, const double& delta_t, const int& nr_Particles);
vector<vector<double>> RK4_field(vector<vector<double>> data_t_n, double delta_t, int nr_Particles);


#endif