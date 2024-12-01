#include <vector>
#include <functional>
#include "functions.hpp"
#include "beschleunigung.hpp"


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
vector<vector<double>> RK4(vector<vector<double>> data_t_n, double delta_t, int nr_Particles) {
    int N = nr_Particles;
    
    vector<vector<double>> data_t_n_1 = zero_2d_arr(N, 7);
    
    vector<vector<double>> r_n(N, vector<double>(3));
    vector<vector<double>> v_n(N, vector<double>(3));
    vector<vector<double>> a_n(N, vector<double>(3));
 
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        r_n[i] = extract_position(data_t_n[i]);
        v_n[i] = extract_velocity(data_t_n[i]);
    }

    a_n = acceleration_parallel(data_t_n);

    vector<vector<double>> r_n_1(N, vector<double>(3));
    vector<vector<double>> v_n_1(N, vector<double>(3));
    vector<vector<double>> tilde_v_1(N, vector<double>(3));
    vector<vector<double>> tilde_r_1(N, vector<double>(3));
    vector<vector<double>> tilde_v_2(N, vector<double>(3));
    vector<vector<double>> tilde_r_2(N, vector<double>(3));
    vector<vector<double>> tilde_v_3(N, vector<double>(3));
    vector<vector<double>> tilde_r_3(N, vector<double>(3));
    vector<vector<double>> tilde_v_4(N, vector<double>(3));
    vector<vector<double>> tilde_r_4(N, vector<double>(3));

    #pragma omp parallel
    {
        vector<vector<double>> intermed(N, vector<double>(7));
        vector<vector<double>> int_acc(N, vector<double>(3));

        #pragma omp for
        for (int i = 0; i < N; i++) {
            tilde_v_1[i] = delta_t * a_n[i];
            tilde_r_1[i] = delta_t * v_n[i];

            for (int j = 0; j < 3; j++) {
                intermed[i][j] = r_n[i][j] + 0.5 * tilde_r_1[i][j];
            }
            int_acc = acceleration_parallel(intermed);

            tilde_v_2[i] = delta_t * int_acc[i];
            tilde_r_2[i] = delta_t * (v_n[i] + 0.5 * tilde_v_1[i]);

            // reset intermediate positions
            for (int j = 0; j < 3; j++) {
                intermed[i][j] = r_n[i][j];
            }
            for (int j = 0; j < 3; j++) {
                intermed[i][j] = r_n[i][j] + 0.5 * tilde_r_2[i][j];
            }
            int_acc = acceleration_parallel(intermed);

            tilde_v_3[i] = delta_t * int_acc[i];
            tilde_r_3[i] = delta_t * (v_n[i] + 0.5 * tilde_v_2[i]);

            // reset intermediate positions
            for (int j = 0; j < 3; j++) {
                intermed[i][j] = r_n[i][j];
            }

            // move particle i to new pos
            for (int j = 0; j < 3; j++) {
                intermed[i][j] = r_n[i][j] + tilde_r_3[i][j];
            }
            int_acc = acceleration_parallel(intermed);

            tilde_v_4[i] = delta_t * int_acc[i];
            tilde_r_4[i] = delta_t * (v_n[i] + tilde_v_3[i]);

            v_n_1[i] = v_n[i] + 1.0 / 6 * (tilde_v_1[i] + tilde_v_4[i]) + 1.0 / 3 * (tilde_v_2[i] + tilde_v_3[i]);
            r_n_1[i] = r_n[i] + 1.0 / 6 * (tilde_r_1[i] + tilde_r_4[i]) + 1.0 / 3 * (tilde_r_2[i] + tilde_r_3[i]);
        }
    }

    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < 3; j++) {
            data_t_n_1[i][j] = r_n_1[i][j];
            data_t_n_1[i][j + 3] = v_n_1[i][j];
        }
        data_t_n_1[i][6] = data_t_n[i][6];
    }

    return data_t_n_1;

}


vector<vector<double>> RK4_field(vector<vector<double>> data_t_n, double delta_t, int nr_Particles) {

    int N = nr_Particles;
    
    vector<vector<double>> data_t_n_1 = zero_2d_arr(N, 7);
    
    vector<vector<double>> r_n(N, vector<double>(3));
    vector<vector<double>> v_n(N, vector<double>(3));
    vector<vector<double>> a_n(N, vector<double>(3));
 
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        r_n[i] = extract_position(data_t_n[i]);
        v_n[i] = extract_velocity(data_t_n[i]);
    }

    a_n = acceleration_parallel(data_t_n);

    vector<vector<double>> r_n_1(N, vector<double>(3));
    vector<vector<double>> v_n_1(N, vector<double>(3));
    vector<vector<double>> tilde_v_1(N, vector<double>(3));
    vector<vector<double>> tilde_r_1(N, vector<double>(3));
    vector<vector<double>> tilde_v_2(N, vector<double>(3));
    vector<vector<double>> tilde_r_2(N, vector<double>(3));
    vector<vector<double>> tilde_v_3(N, vector<double>(3));
    vector<vector<double>> tilde_r_3(N, vector<double>(3));
    vector<vector<double>> tilde_v_4(N, vector<double>(3));
    vector<vector<double>> tilde_r_4(N, vector<double>(3));

    #pragma omp parallel
    {
        

        #pragma omp for
        for (int i = 0; i < N; i++) {
            function<vector<double>(const int&, const vector<double>&)> acc_field = acceleration_field_particle_i(data_t_n);

            tilde_v_1[i] = delta_t * a_n[i];
            tilde_r_1[i] = delta_t * v_n[i];

            // for (int j = 0; j < 3; j++) {
            //     intermed[i][j] = r_n[i][j] + 0.5 * tilde_r_1[i][j];
            // }
            // int_acc = acceleration_parallel(intermed);

            // tilde_v_2[i] = delta_t * int_acc[i];
            tilde_v_2[i] = delta_t * acc_field(i, r_n[i] + 0.5 * tilde_r_1[i]);
            tilde_r_2[i] = delta_t * (v_n[i] + 0.5 * tilde_v_1[i]);

            // // reset intermediate positions
            // for (int j = 0; j < 3; j++) {
            //     intermed[i][j] = r_n[i][j];
            // }
            // for (int j = 0; j < 3; j++) {
            //     intermed[i][j] = r_n[i][j] + 0.5 * tilde_r_2[i][j];
            // }
            // int_acc = acceleration_parallel(intermed);

            tilde_v_3[i] = delta_t * acc_field(i,r_n[i] + 0.5 * tilde_r_2[i]);
            tilde_r_3[i] = delta_t * (v_n[i] + 0.5 * tilde_v_2[i]);

            // // reset intermediate positions
            // for (int j = 0; j < 3; j++) {
            //     intermed[i][j] = r_n[i][j];
            // }

            // // move particle i to new pos
            // for (int j = 0; j < 3; j++) {
            //     intermed[i][j] = r_n[i][j] + tilde_r_3[i][j];
            // }
            // int_acc = acceleration_parallel(intermed);

            tilde_v_4[i] = delta_t * acc_field(i, r_n[i] + tilde_r_3[i]);
            tilde_r_4[i] = delta_t * (v_n[i] + tilde_v_3[i]);

            v_n_1[i] = v_n[i] + 1.0 / 6 * (tilde_v_1[i] + tilde_v_4[i]) + 1.0 / 3 * (tilde_v_2[i] + tilde_v_3[i]);
            r_n_1[i] = r_n[i] + 1.0 / 6 * (tilde_r_1[i] + tilde_r_4[i]) + 1.0 / 3 * (tilde_r_2[i] + tilde_r_3[i]);
        }
    }

    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < 3; j++) {
            data_t_n_1[i][j] = r_n_1[i][j];
            data_t_n_1[i][j + 3] = v_n_1[i][j];
        }
        data_t_n_1[i][6] = data_t_n[i][6];
    }

    return data_t_n_1;

}