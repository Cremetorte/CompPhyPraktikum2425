#include <cmath>
#include <vector>
#include <stdexcept>
#include "functions.hpp"
#include <iostream>
#include "beschleunigung.hpp"
#include "ruck.hpp"

using namespace std;



vector<vector<double>> hermite_iteriert(vector<vector<double>> table, double delta_t, int nr_Particles) {
    static int iterationCount = 0;
    // cout << iterationCount;

    // Make only 2 iterations
    if (iterationCount >= 2) {
        iterationCount = 0;
        return table;
    }

    iterationCount++;
    
    // Rename nr of particles
    int N = nr_Particles;
    
    // Initialize output table
    vector<vector<double>> data_t_n_1 = zero_2d_arr(N, 7);

    // Initialize predicted table
    vector<vector<double>> data_p_t_n_1 = zero_2d_arr(N, 7);
    
    // Prepare Data: Extract last N Rows
    if (table.size() < N) {
        throw std::out_of_range("Table size is smaller than nr_particles");
    }
    vector<vector<double>> data_t_n(table.end() - N, table.end());

    // Initialize all needed quantities at t=t_n
    vector<vector<double>> r_n;
    vector<vector<double>> v_n;
    vector<vector<double>> a_n;
    vector<vector<double>> j_n; // j for jerk

    // Extract r_n
    for (vector<double> particle : data_t_n) {
        r_n.push_back(extract_position(particle));
    }
    // Extract v_n
    for (vector<double> particle : data_t_n) {
        v_n.push_back(extract_velocity(particle));
    }
    // Calculate a_n, j_n
    a_n = acceleration(data_t_n);
    j_n = jerk(data_t_n);

    // Initialize all quantities to be calculated, t=n+1
    vector<vector<double>> rp_n_1;
    vector<vector<double>> vp_n_1;
    vector<vector<double>> ap_n_1;
    vector<vector<double>> jp_n_1;

    // Calculate vp_n_1
    for (int i = 0; i < N; i++) {
        vector<double> new_vel_p = {0, 0, 0};

        new_vel_p = v_n[i] + delta_t * a_n[i] + 0.5 * (delta_t * delta_t) * j_n[i];

        vp_n_1.push_back(new_vel_p);
    }

    // Calculate rp_n_1
    for (int i = 0; i < N; i++) {
        vector<double> new_pos_p = {0, 0, 0};

        new_pos_p = r_n[i] + delta_t * v_n[i] + 0.5 * (delta_t * delta_t) * a_n[i] + 1.0 / 6 * (delta_t * delta_t * delta_t) * j_n[i];

        rp_n_1.push_back(new_pos_p);
    }

    // Push rp_n_1 and masses to output in order to calculate ap_n+1
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < 3; j++) {
            data_p_t_n_1[i][j] = rp_n_1[i][j];
        }
        data_p_t_n_1[i][6] = data_t_n[i][6];
    }

    // Calculate ap_n+1
    ap_n_1 = acceleration(data_p_t_n_1);

    // Push vp_n_1 to output in order to calculate jp_n+1
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < 3; j++) {
            data_p_t_n_1[i][j + 3] = vp_n_1[i][j];
        }
    }

    // Calculate jp_n+1
    jp_n_1 = jerk(data_p_t_n_1);

    // Initialize corrected values
    vector<vector<double>> rc_n_1;
    vector<vector<double>> vc_n_1;

    // Calculate vc_n_1
    for (int i = 0; i < N; i++) {
        vector<double> new_vel_c = {0, 0, 0};

        new_vel_c = v_n[i] + 0.5 * delta_t * (ap_n_1[i] + a_n[i]) + 1.0 / 12 * pow(delta_t, 2) * (jp_n_1[i] - j_n[i]);

        vc_n_1.push_back(new_vel_c);
    }

    // Calculate rc_n_1
    for (int i = 0; i < N; i++) {
        vector<double> new_pos_c = {0, 0, 0};

        new_pos_c = r_n[i] + 0.5 * delta_t * (vc_n_1[i] + v_n[i]) + 1.0 / 12 * pow(delta_t, 2) * (ap_n_1[i] - a_n[i]);

        rc_n_1.push_back(new_pos_c);
    }

    // Push rc_n_1 and masses to output
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < 3; j++) {
            data_t_n_1[i][j] = rc_n_1[i][j];
        }
        data_t_n_1[i][6] = data_t_n[i][6];
    }

    // Push vc_n_1 to output
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < 3; j++) {
            data_t_n_1[i][j + 3] = vc_n_1[i][j];
        }
    }

    // vector<vector<double>> copy = data_t_n_1;
    // print_data(copy);

    return hermite_iteriert(data_t_n_1, delta_t, N);
}

// vector<vector<double>> hermite_iteriert(vector<vector<double>> table, double delta_t, int nr_Particles) {
//     return hermite_iteriert_rec(table, delta_t, nr_Particles);
// }