#include <iostream>
#include <vector>
#include <cmath>
#include "functions.hpp"

using namespace std;


vector<vector<double>> acceleration(vector<vector<double>> table){
    vector<double> a_i;
    vector<double> a_i_one_term;
    vector<vector<double>> acc_matrix;
    for(vector<double> particle_i : table){
        a_i = {0,0,0};
        a_i_one_term = {0,0,0};
        //vector<double> r_i = {particle_i[0],particle_i[1],particle_i[2]};
        vector<double> r_i = extract_position(particle_i);
        for(vector<double> particle_j : table){
            if(particle_i == particle_j){
                continue;
            }
            //vector<double> r_j = {particle_j[0],particle_j[1],particle_j[2]};
            vector<double> r_j = extract_position(particle_j);
            vector<double> r_ij = subtract_vectors(r_j,r_i);
            double r_ij_absolute = pow(absolute_value(r_ij), 3);
            a_i_one_term = scalar_multiplication((particle_j[6]/r_ij_absolute), r_ij);
            a_i = add_vectors(a_i, a_i_one_term);
             
        }
        acc_matrix.push_back(a_i);
    }
    return acc_matrix;
}