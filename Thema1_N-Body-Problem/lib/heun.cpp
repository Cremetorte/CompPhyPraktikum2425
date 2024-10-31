#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "import.hpp"

using namespace std;


/**
 * @brief Evolves the state by one timestep.
 * 
 * Uses Heun's method to evolve a state by one timestep.
 * 
 * @param table Raw input of the states at t_n.
 * @param delta_t Length of timesteps.
 * @param nr_particles Number of particles N.
 * @return A 2D vector of doubles representing the calculated state at t_n+1.
 */
vector<vector<double>> heun(vector<vector<double>> table, double delta_t, int nr_Particles) {
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


    //initialize all quantities to be calculated, t=n+1
    vector<vector<double>> r_n_1;
    vector<vector<double>> v_n_1;
    vector<vector<double>> a_n_1;


    //initialize intermediate variables

    //tilde_v_1 = delta_t*a_n
    vector<vector<double>> tilde_v_1;
    //tilde_r_1 = delta_t*v_n
    vector<vector<double>> tilde_r_1;
    //tilde_v_2 = delta_t*a(r_n + tilde_r_1)
    vector<vector<double>> tilde_v_2;
    //tilde_r_2 = delta_t*(v_n + tilde_v_1)
    vector<vector<double>> tilde_r_2;

    //calculate intermediate variables
    for (int i=0; i<N; i++) {
        tilde_v_1.push_back(scalar_multiplication(delta_t, a_n[i]));
        tilde_r_1.push_back(scalar_multiplication(delta_t, v_n[i]));
    }

    //calculate a(r_n + tilde_r_1)
    //prepare 2d matrix in the usual format
    vector<vector<double>> intermed = zero_2d_arr(N,7);
    for (int i=0; i<N; i++){
        for (int j=0; j<N; j++) {
            intermed[i][j] = add_vectors(r_n[i], tilde_r_1[i])[j];
        }
        intermed[i][6]  = data_t_n[i][6];
    }
    vector<vector<double>> int_acc = acceleration(intermed);

    //calculate tilde_v_2 = delta_t*a(r_n + tilde_r_1)
    for (int i=0; i<N; i++) {
        tilde_v_2.push_back(scalar_multiplication(delta_t, int_acc[i]));
        tilde_r_2.push_back(scalar_multiplication(delta_t, add_vectors(r_n[i], tilde_r_1[i])));
    }

    //calculate r_n+1 and v_n+1:
    for (int i=0; i<N; i++) {
        v_n_1.push_back(add_vectors(v_n[i], scalar_multiplication(0.5, add_vectors(tilde_v_1[i], tilde_v_2[i]))));
        r_n_1.push_back(add_vectors(r_n[i], scalar_multiplication(0.5, add_vectors(tilde_r_1[i], tilde_r_2[i]))));
    }

    //push r_n+1 and v_n+1 to output
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<3; j++) {
            data_t_n_1[i][j] = r_n_1[i][j];
            data_t_n_1[i][j+3] = v_n_1[i][j];
        }
    }
    return data_t_n_1;
}