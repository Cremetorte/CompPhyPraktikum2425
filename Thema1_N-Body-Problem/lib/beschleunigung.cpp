#include <iostream>
#include <vector>
#include <cmath>

using namespace std;


vector<vector<double>> acceleration(vector<vector<double>> table){
    vector<double> a_i;
    vector<vector<double>> acc_matrix;
    for(vector<double> particle_i : table){
        vector<double> r_i = {particle_i[0],particle_i[1],particle_i[2]};
        for(vector<double> particle_j : table){
            if(particle_i == particle_j){
                continue;
            }
            vector<double> r_j = {particle_j[0],particle_j[1],particle_j[2]};
            a_i = particle_j[6] ;
        }
    }
}