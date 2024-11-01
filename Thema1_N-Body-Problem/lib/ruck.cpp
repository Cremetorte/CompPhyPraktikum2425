#include <iostream>
#include <vector>
#include <cmath>
#include "functions.hpp"

using namespace std;


vector<vector<double>> jerk(vector<vector<double>> table){
    // initialize vectors and output
    vector<double> jerk_i;
    vector<double> jerk_i_one_term;
    vector<vector<double>> jerk_matrix;

    for(vector<double> particle_i : table){
        //set jerk_i to 0
        jerk_i = {0,0,0};
        jerk_i_one_term = {0,0,0};

        //set r_i, v_i
        vector<double> r_i = extract_position(particle_i);
        vector<double> v_i = extract_velocity(particle_i);

        for(vector<double> particle_j : table){

            //check if i and j are the same (elementwise)
            if(particle_i == particle_j){
                continue;
            }

            //set r_j, r_ij, v_j, v_ij
            vector<double> r_j = extract_position(particle_j);
            vector<double> r_ij = subtract_vectors(r_j,r_i);
            vector<double> v_j = extract_velocity(particle_j);
            vector<double> v_ij = subtract_vectors(v_j,v_i);

            //calc denominator r_ij^3
            double r_ij_absolute_3 = pow(absolute_value(r_ij), 3);
            //calc denominator r_ij^5
            double r_ij_absolute_5 = pow(absolute_value(r_ij), 5);
            //mass of particle
            double m = particle_j[6];
            //calc denominator v_ij * r_ij
            double product_v_r = scalar_product(v_ij, r_ij);

            //calc term in brackets
            vector<double> bracket_term1 = scalar_multiplication(1/r_ij_absolute_3, v_ij);
            vector<double> bracket_term2 = scalar_multiplication((3*product_v_r/r_ij_absolute_5), r_ij);
            vector<double> bracket = subtract_vectors(bracket_term1, bracket_term2);

            //calculate acceleration from particle j
            jerk_i_one_term = scalar_multiplication(m, bracket);

            //add to total accerleration of particle i
            jerk_i = add_vectors(jerk_i, jerk_i_one_term);
             
        }
        jerk_matrix.push_back(jerk_i);
    }
    return jerk_matrix;

}
