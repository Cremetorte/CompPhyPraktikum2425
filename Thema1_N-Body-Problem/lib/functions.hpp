#ifndef FUNCTIONS_HPP
#define FUNCTIONS_HPP

#include <vector>
#include <iostream>
#include <math.h>
#include "functions.cpp"
using namespace std;


// declare the functions here
vector<double> add_vectors(const vector<double>& v_1, const vector<double>& v_2);
vector<double> scalar_multiplication(double c, vector<double> vec);
vector<double> subtract_vectors(vector<double> v_1, vector<double> v_2);
vector<double> extract_position(vector<double> raw_data_row);
vector<double> extract_velocity(vector<double> raw_data_row);
double absolute_value(vector<double> vec);
vector<double> calc_COM(vector<vector<double>> data);
void print_Vector(vector<double> vec);



#endif