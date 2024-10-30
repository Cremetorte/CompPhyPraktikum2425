#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "import.hpp"

using namespace std;


/**
 * @brief Evolves the state by one timestep.
 * 
 * Uses the Velocity-Verlet time integrator to evolve a N-particle state by one timestep from t_n to t_n+1.
 * 
 * @param table Raw input of the states at t_n.
 * @param delta_t Length of timesteps.
 * @param nr_particles Number of particles N.
 * @return A 2D vector of doubles representing the calculated state at t_n+1.
 */
vector<vector<double>> velocity_verlet(vector<vector<double>> table, double delta_t, int nr_particles) {
    bool log = false;
    
    //Check if N is positive
    if (nr_particles <= 0) {
        throw std::invalid_argument("nr_particles must be positive");
    }
    
    
    //Check if there are enough Rows/Particles
    int table_size = table.size();
    if (table_size < nr_particles) {
        throw std::out_of_range("Table size is smaller than nr_particles");
    }


    //Extract the last N Rows
    vector<vector<double>> table_t_n;
    for (int i = table_size - nr_particles; i < table_size; i++) {
        table_t_n.push_back(table[i]);
    }

    
    //initialize output
    vector<vector<double>> table_t_n_1 = zero_2d_arr(nr_particles,7);

    //initialize Positions and velocities at t_n
    vector<vector<double>> pos_t_n;
    vector<vector<double>> vel_t_n;
    vector<vector<double>> acc_t_n;

    //initialize Positions and velocities at t_n+1
    vector<vector<double>> pos_t_n_1;
    vector<vector<double>> vel_t_n_1;
    vector<vector<double>> acc_t_n_1;


    //Extract Posiitons and Velocities at t_n
    for (vector<double> particle : table_t_n) {
        pos_t_n.push_back(extract_position(particle));
    }
    for (vector<double> particle : table_t_n) {
        vel_t_n.push_back(extract_velocity(particle));
    }
    if (log) {
        cout << "positions at t_n:" << endl;
        print_data(pos_t_n);
        cout << "velocities at t_n:" << endl;
        print_data(vel_t_n);
    }
    


    //calculate accelerations at t_n
    acc_t_n = acceleration(table_t_n);
    if (log) {
        cout << "Accelerations at t_n:" << endl;
        print_data(acc_t_n);
    }
    
    
    //calculate all r_n+1
    for (int particle_ind = 0; particle_ind < nr_particles; particle_ind++) {
        vector<double> new_pos = pos_t_n[particle_ind];

        vector<double> v_part = scalar_multiplication(delta_t, vel_t_n[particle_ind]);

        double coeff = delta_t*delta_t*0.5;
        vector<double> a_part = scalar_multiplication(coeff, acc_t_n[particle_ind]);

        new_pos = add_vectors(new_pos, v_part);
        new_pos = add_vectors(new_pos, a_part);

        if (log) {
            cout << "Particle " << particle_ind << ": " << endl << "v_n*delta_t = ";
            print_Vector(v_part);

            cout << "1/2*delta_t^2*a_n = ";
            print_Vector(a_part);

            cout << "New Position " << endl;
            print_Vector(new_pos);
        }

        pos_t_n_1.push_back(new_pos);
        
    }

    //push r_n+1 and masses to output
    for (int particle_ind = 0; particle_ind < nr_particles; particle_ind++) {
        for (int i=0;i<3;i++) {
            table_t_n_1[particle_ind][i] = pos_t_n_1[particle_ind][i];
            table_t_n_1[particle_ind][6] = table_t_n[particle_ind][6];
        }
    }

    if (log) {
        cout << "table_t_n_1: " << endl;
        print_data(table_t_n_1);
    }
    
    //get a_n+1
    acc_t_n_1 = acceleration(table_t_n_1);
    
    
    if (log) {
        cout << "acceleration at t_n+1: " << endl;
        print_data(table_t_n_1);
    }

    //calculate all v_n+1
    for (int particle_ind = 0; particle_ind < nr_particles; particle_ind++) {
        vector<double> new_vel = vel_t_n[particle_ind];

        double coeff = 0.5*delta_t;
        vector<double> a_tot = add_vectors(acc_t_n[particle_ind], acc_t_n_1[particle_ind]);
        a_tot = scalar_multiplication(coeff, a_tot);

        new_vel = add_vectors(new_vel, a_tot);
        
        if (log) {
            cout << "New Velocity of Particle " << particle_ind << endl;
            print_Vector(new_vel);
        }

        vel_t_n_1.push_back(new_vel);
    }
    

    //push v_n+1 to output
    for (int particle_ind = 0; particle_ind < nr_particles; particle_ind++) {
        for (int i=3;i<6;i++) {
            table_t_n_1[particle_ind][i] = pos_t_n_1[particle_ind][i-3];
        }
    }

    if (log) {
        cout << "complete data: " << endl;
        print_data(table_t_n_1);
    }

    return table_t_n_1;
    
}