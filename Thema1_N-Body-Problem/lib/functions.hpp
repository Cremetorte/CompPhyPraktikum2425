#ifndef FUNCTIONS_HPP
#define FUNCTIONS_HPP

#include <vector>
#include <iostream>
#include <math.h>
#include "functions.cpp"
using namespace std;


// declare the functions here
vector<double> add_vectors(const vector<double>& v_1, const vector<double>& v_2);
double scalar_product(const vector<double>& v_1, const vector<double>& v_2);
vector<double> scalar_multiplication(const double& c, const vector<double>& vec);
vector<double> subtract_vectors(const vector<double>& v_1, const vector<double>& v_2);
vector<double> extract_position(const vector<double>& raw_data_row);
vector<double> extract_velocity(const vector<double>& raw_data_row);
double absolute_value(const vector<double>& vec);
vector<double> calc_COM(const vector<vector<double>>& data);
void print_Vector(vector<double> vec);
vector<vector<double>> zero_2d_arr(int rows, int cols);
vector<double> dimensions(vector<vector<double>> double_vector);
double nearly_zero_to_zero(double value);

//Operatoren
vector<double> operator+(const vector<double>& a, const vector<double>& b);
vector<double> operator-(const vector<double>& a, const vector<double>& b);
vector<double> operator*(const double& a, const vector<double>& b);


#endif