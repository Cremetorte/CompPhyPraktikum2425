#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "import.hpp"

using namespace std;


/**
 * @brief Evolves the state by one timestep.
 * 
 * Uses the Runge-Ketta 4 algorithm to evolve a state by one timestep.
 * 
 * @param table Raw input of the states at t_n.
 * @param delta_t Length of timesteps.
 * @param nr_particles Number of particles N.
 * @return A 2D vector of doubles representing the calculated state at t_n+1.
 */
vector<vector<double>> RK4(vector<vector<double>> table, double delta_t, int nr_Particles) {
    //rename nr of particles
    int N = nr_Particles;
    
    //initialize output table
    vector<vector<double>> data_t_n_1 = zero_2d_arr(N,7);
    
    //Prepare Data: Extract last N Rows
    if (table.size() < N) {
        throw std::out_of_range("Table size is smaller than nr_particles");
    }
    vector<vector<double>> data_t_n(table.end() - N, table.end()); 

    //initialize all needed quantities at t=t_n
    vector<vector<double>> r_n;
    vector<vector<double>> v_n;
    vector<vector<double>> a_n;
 
    //extract r_n and v_n
    for (vector<double> particle : data_t_n) {
        r_n.push_back(extract_position(particle));
        v_n.push_back(extract_velocity(particle));
    }

    //calculate a_n
    a_n = acceleration(data_t_n);

    // cout << "acceleration at t_n:" << endl;
    // print_data(a_n);
    // cout << endl;


    //initialize all quantities to be calculated, t=n+1
    vector<vector<double>> r_n_1;
    vector<vector<double>> v_n_1;


    //initialize intermediate variables

    //tilde_v_1 = delta_t*a_n
    vector<vector<double>> tilde_v_1;
    //tilde_r_1 = delta_t*v_n
    vector<vector<double>> tilde_r_1;
    //tilde_v_2 = delta_t*a(r_n + 0.5*tilde_r_1)
    vector<vector<double>> tilde_v_2;
    //tilde_r_2 = delta_t*(v_n + 0.5*tilde_v_1)
    vector<vector<double>> tilde_r_2;
    //tilde_v_3 = delta_t*a(r_n + 0.5*tilde_r_2)
    vector<vector<double>> tilde_v_3;
    //tilde_r_3 = delta_t*(v_n + 0.5*tilde_v_2)
    vector<vector<double>> tilde_r_3;
    //tilde_v_4 = delta_t*a(r_n + tilde_r_3)
    vector<vector<double>> tilde_v_4;
    //tilde_r_4 = delta_t*(v_n + tilde_v_3)
    vector<vector<double>> tilde_r_4;

    //initialize intermediate table for acceleration
    vector<vector<double>> data_temp;
    vector<vector<double>> acc_temp;

    //calculate intermediate variables
    //tilde_r_1 and tilde_r_2:
    for (int i = 0; i<N; i++) {
        tilde_v_1.push_back(scalar_multiplication(delta_t, a_n[i]));
        tilde_r_1.push_back(scalar_multiplication(delta_t, v_n[i]));
    }



}