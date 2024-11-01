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
    vector<vector<double>> intermed = data_t_n;
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



    //calculate intermediate variables
    for (int i = 0; i<N; i++) {
        //tilde_r_1 and tilde_r_2:
        tilde_v_1.push_back(delta_t * a_n[i]);
        tilde_r_1.push_back(delta_t * v_n[i]);

        //move only particle i  to  r_n + 0.5*tilde_r_1 to calculate a(r_n + tilde_r_1)
        for (int j=0; j<3; j++) {
            intermed[i][j] = (r_n[i] + (0.5 * tilde_r_1[i]))[j];
        }
        //calculate a(r_n + tilde_r_1)
        vector<vector<double>> int_acc = acceleration(intermed);

        //calculate tilde_v_2:
        tilde_v_2.push_back(delta_t * int_acc[i]);

        //calculate tilde_r_2
        tilde_r_2.push_back(delta_t * (v_n[i] + 0.5 * tilde_v_1[i]));



        //reset intermediate positions to t_n
        intermed = data_t_n;
        //move only particle i  to  r_n + 0.5*tilde_r_2 to calculate a(r_n + 0.5 tilde_r_2)
        for (int j=0; j<3; j++) {
            intermed[i][j] = (r_n[i] + (0.5 * tilde_r_2[i]))[j];
        }
        //calculate a(r_n + 0.5*tilde_r_2)
        int_acc = acceleration(intermed);

        //calculate tilde_v_3:
        tilde_v_3.push_back(delta_t * int_acc[i]);

        //calculate tilde_r_3
        tilde_r_3.push_back(delta_t * (v_n[i] + 0.5 * tilde_v_2[i]));



        //reset intermediate positions to t_n
        intermed = data_t_n;
        //move only particle i  to  r_n + tilde_r_3 to calculate a(r_n + tilde_r_3)
        for (int j=0; j<3; j++) {
            intermed[i][j] = (r_n[i] + tilde_r_3[i])[j];
        }
        //calculate a(r_n + tilde_r_3)
        int_acc = acceleration(intermed);

        //calculate tilde_v_4:
        tilde_v_4.push_back(delta_t * int_acc[i]);

        //calculate tilde_r_4
        tilde_r_4.push_back(delta_t * (v_n[i] + tilde_v_3[i]));
        

        //calculate v_n+1, r_n+1
        v_n_1.push_back(v_n[i] + 1.0/6 * (tilde_v_1[i] + tilde_v_4[i]) + 1.0/3 * (tilde_v_2[i] + tilde_v_3[i]));
        r_n_1.push_back(r_n[i] + 1.0/6 * (tilde_r_1[i] + tilde_r_4[i]) + 1.0/3 * (tilde_r_2[i] + tilde_r_3[i]));
    }

    
    //push r_n+1, v_n+1 and masses to output
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<3; j++) {
            data_t_n_1[i][j] = r_n_1[i][j];
            data_t_n_1[i][j+3] = v_n_1[i][j];
            data_t_n_1[i][6] = data_t_n[i][6];
        }
    }

    return data_t_n_1;

}