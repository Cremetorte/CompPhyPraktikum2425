#ifndef EULER_CROMER_HPP
#define EULER_CROMER_HPP

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include "euler-cromer.cpp"


// declare the functions here
vector<vector<double>> euler_cromer(vector<vector<double>> table, double delta_t, int nr_Particles);

#endif