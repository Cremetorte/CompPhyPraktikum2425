#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "import.hpp"

using namespace std;



vector<vector<double>> velocity_verlet(vector<vector<double>> table, double delta_t, int nr_Particles) {
    //extract only the last N rows (t_n)
    vector<vector<double>> table_t_n;
    int table_size = table.size();
    //cout << table_size;

    for (int i = table_size - nr_Particles; i < table_size; i++) {
        table_t_n.push_back(table[i]);
    }

    //print_data(table_t_n);
    
    //initialize output
    vector<vector<double>> table_t_n_1 = zero_2d_arr(nr_Particles,7);
    //print_data(table_t_n_1);

    //initialize Positions and velocities at t_n
    vector<vector<double>> pos_t_n;
    vector<vector<double>> vel_t_n;
    vector<vector<double>> acc_t_n;

    //initialize Positions and velocities at t_n+1
    vector<vector<double>> pos_t_n_1;
    vector<vector<double>> vel_t_n_1;
    vector<vector<double>> acc_t_n_1;


    //compute Posiitons and Velocities at t_n
    for (vector<double> particle : table_t_n) {
        pos_t_n.push_back(extract_position(particle));
    }
    for (vector<double> particle : table_t_n) {
        vel_t_n.push_back(extract_velocity(particle));
    }
    acc_t_n = acceleration(table_t_n); //needs to be implemented
    
    
    
    //calculate all r_n+1
    for (int particle_ind = 0; particle_ind < nr_Particles; particle_ind++) {
        vector<double> new_pos = add_vectors(pos_t_n[particle_ind], scalar_multiplication(delta_t, vel_t_n[particle_ind]));
        new_pos = add_vectors(new_pos, scalar_multiplication(0.5 * delta_t * delta_t, acc_t_n[particle_ind]));
        pos_t_n_1.push_back(new_pos);
    }

    //push r_n+1 and masses to output
    for (int particle_ind = 0; particle_ind < nr_Particles; particle_ind++) {
        for (int i=0;i<3;i++) {
            table_t_n_1[particle_ind][i] = pos_t_n_1[particle_ind][i];
            table_t_n_1[particle_ind][6] = table_t_n[particle_ind][6];
        }
    }

    //get a_n+1
    acc_t_n_1 = acceleration(table_t_n_1);
    //print_data(acc_t_n_1);

    //calculate all v_n+1
    for (int particle_ind = 0; particle_ind < nr_Particles; particle_ind++) {
        vector<double> new_vel = scalar_multiplication(1/2*delta_t, add_vectors(acc_t_n[particle_ind], acc_t_n_1[particle_ind]));
        new_vel = add_vectors(new_vel, vel_t_n[particle_ind]);
    }

    //push v_n+1 to output
    for (int particle_ind = 0; particle_ind < nr_Particles; particle_ind++) {
        for (int i=3;i<6;i++) {
            table_t_n_1[particle_ind][i] = pos_t_n_1[particle_ind][i-3];
        }
    }

    return table_t_n_1;
    
}