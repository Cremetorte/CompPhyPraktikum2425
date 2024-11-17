#include <iostream>
#include <vector>
#include <cmath>
#include <omp.h>
#include <functional>
#include "functions.hpp" // Assuming this header contains the necessary function declarations

using namespace std;


vector<vector<double>> acceleration(vector<vector<double>> table){
    //initialize vectors and output
    vector<double> a_i;
    vector<double> a_i_one_term;
    vector<vector<double>> acc_matrix;
    vector<double> r_i;
    vector<double> r_j;
    vector<double> r_ij;
    double r_ij_absolute;


    for(vector<double> particle_i : table){
        //set a_i to 0
        a_i = {0,0,0};
        a_i_one_term = {0,0,0};
        //set r_i
        r_i = extract_position(particle_i);

        for(vector<double> particle_j : table){

            //check if i and j are the same (elementwise)
            if(particle_i == particle_j){
                continue;
            }

            //set r_j, r_ij
            r_j = extract_position(particle_j);
            r_ij = subtract_vectors(r_j,r_i);

            //calc denominator r_ij^3
            r_ij_absolute = pow(absolute_value(r_ij), 3);

            //calculate acceleration from particle j
            a_i_one_term = scalar_multiplication(((double)particle_j[6]/r_ij_absolute), r_ij);

            //add to total accerleration of particle i
            a_i = add_vectors(a_i, a_i_one_term);
             
        }
        acc_matrix.push_back(a_i);
    }
    return acc_matrix;
}



vector<vector<double>> acceleration_parallel(const vector<vector<double>>& table) {
    int N = table.size();
    
    vector<vector<double>> acc_matrix = zero_2d_arr(N, 3);

    #pragma omp parallel
    {
        // Thread-local storage to avoid frequent allocation and deallocation
        vector<double> a_i(3, 0.0);
        vector<double> a_i_one_term(3, 0.0);
        vector<double> r_i(3, 0.0);
        vector<double> r_j(3, 0.0);
        vector<double> r_ij(3, 0.0);
        double r_ij_absolute;

        #pragma omp for
        for (int i = 0; i < N; i++) {
            // Set a_i to 0
            fill(a_i.begin(), a_i.end(), 0.0);
            fill(a_i_one_term.begin(), a_i_one_term.end(), 0.0);

            // Set r_i
            r_i = extract_position(table[i]);

            #pragma omp parallel for 
            for (int j = 0; j < N; j++) {
                if (i == j) continue;

                // Set r_j, r_ij
                r_j = extract_position(table[j]);
                r_ij = subtract_vectors(r_j, r_i);

                // Calculate denominator r_ij^3
                r_ij_absolute = pow(absolute_value(r_ij), 3);

                // Calculate acceleration from particle j
                a_i_one_term = scalar_multiplication(table[j][6] / r_ij_absolute, r_ij);

                // Add to total acceleration of particle i
                a_i = add_vectors(a_i, a_i_one_term);
            }

            // Store the result in the acceleration matrix
            acc_matrix[i] = a_i;
        }
    }

    return acc_matrix;
}




function<vector<double>(const int&, const vector<double>&)> acceleration_field_particle_i(const vector<vector<double>>& table) {
    return [&table](const int& i, const vector<double>& r) -> vector<double> {
        
        auto acc_field_j = [&table](const int& j, const vector<double>& r) -> vector<double> {
            vector<double> acc;
            vector<double> diff_r = r - extract_position(table[j]);
            double distance = absolute_value(diff_r);

            acc = -(table[j][6] / pow(absolute_value(diff_r), 3)) * diff_r;

            return acc;
        };

        vector<double> acc(3, 0.0);

        #pragma omp parallel for
        for (int j=0; j<table.size(); j++) {
            if (j == i) {
                continue;
            }

            acc = acc + acc_field_j(j, r);

        }

        return acc;
    };
}