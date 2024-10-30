//#include "functions.hpp"
#include <vector>
#include <iostream>
#include <math.h>
#include <iomanip>


using namespace std;


vector<double> add_vectors(const vector<double>& v_1, const vector<double>& v_2) {
    int size1 = v_1.size();
    vector<double> finalVec;
    
    if (size1 != v_2.size()) {
        cout << "Error: Vectors need to be the same dimension!";
    }

    for (int i = 0; i < size1; i++) {
        finalVec.push_back(v_1[i] + v_2 [i]);

    }

    return finalVec;
}

vector<double> scalar_multiplication(double c, vector<double> vec) {
    vector<double> final_vec;
    
    for (int i = 0; i < vec.size(); i++) {
        final_vec.push_back(c*vec[i]);
    }

    return final_vec;

}

vector<double> subtract_vectors(vector<double> v_1, vector<double> v_2) {
    v_2 = scalar_multiplication(-1, v_2);
    return add_vectors(v_1,v_2);

}

vector<double> extract_position(vector<double> raw_data_row) {
    vector<double> final_vec = {raw_data_row[0], raw_data_row[1], raw_data_row[2]};
    return final_vec;
}

vector<double> extract_velocity(vector<double> raw_data_row) {
    vector<double> final_vec = {raw_data_row[3], raw_data_row[4], raw_data_row[5]};
    return final_vec;
}

double absolute_value(vector<double> vec) {
    double abs = 0;
    for (int i = 0; i<vec.size(); i++) {
        abs += vec[i]*vec[i];
    }
    return pow(abs, 0.5);
}


vector<double> calc_COM(vector<vector<double>> data) {
    vector<double> COM = {0,0,0};

    for (vector<double> particle_i : data) {
        COM = add_vectors(scalar_multiplication(particle_i[6], extract_position(particle_i)), COM);
    }

    return COM;
}

void print_Vector(vector<double> vec) {
    for (double i : vec) {
        cout << setprecision(16) << i << ",";
    }
    cout << endl;
}

vector<vector<double>> zero_2d_arr(int rows, int cols) {
    vector<vector<double>> output;
    vector<double> zero_row;

    for (int i=0; i<cols; i++) {
        zero_row.push_back(0);
    }
    for(int i=0; i<rows;i++) {
        output.push_back(zero_row);
    }

    return output;
}

vector<double> dimensions(vector<vector<double>> double_vector) {
    vector<double> ret_vec;
    ret_vec.push_back(double_vector.size());
    ret_vec.push_back(double_vector[0].size());
    return ret_vec;
}


double nearly_zero_to_zero(double value) {
    return (std::abs(value) < std::numeric_limits<double>::epsilon()) ? 0.0 : value;
}