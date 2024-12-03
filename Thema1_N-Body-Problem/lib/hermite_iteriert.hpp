#ifndef HERMITE_iteriert_HPP
#define HERMITE_iteriert_HPP

#include <vector>


using namespace std;


// declare the functions here

// vector<vector<double>> hermite_iteriert_rec(vector<vector<double>> table, double delta_t, int nr_Particles, int iterationCount = 0);
vector<vector<double>> hermite_iteriert(vector<vector<double>> table, double delta_t, int nr_Particles);

#endif