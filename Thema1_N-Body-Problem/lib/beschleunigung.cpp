#include <iostream>
#include <vector>
#include <cmath>
#include "functions.hpp"

using namespace std;


vector<vector<double>> acceleration(vector<vector<double>> table){
    //initialize vectors and output
    vector<double> a_i;
    vector<double> a_i_one_term;
    vector<vector<double>> acc_matrix;

    for(vector<double> particle_i : table){
        //set a_i to 0
        a_i = {0,0,0};
        a_i_one_term = {0,0,0};

        //set r_i
        vector<double> r_i = extract_position(particle_i);

        for(vector<double> particle_j : table){

            //check if i and j are the same (elementwise)
            if(particle_i == particle_j){
                continue;
            }

            //set r_j, r_ij
            vector<double> r_j = extract_position(particle_j);
            vector<double> r_ij = subtract_vectors(r_j,r_i);

            //calc denominator r_ij^3
            double r_ij_absolute = pow(absolute_value(r_ij), 3);

            //calculate acceleration from particle j
            a_i_one_term = scalar_multiplication(((double)particle_j[6]/r_ij_absolute), r_ij);

            //add to total accerleration of particle i
            a_i = add_vectors(a_i, a_i_one_term);
             
        }
        acc_matrix.push_back(a_i);
    }
    return acc_matrix;
}