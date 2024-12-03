#include <iostream>
#include <cmath>
#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "ruck.hpp"

using namespace std;

vector<vector<double>> hermite(vector<vector<double>> table, double delta_t, int nr_Particles) {
    //rename nr of particles
    int N = nr_Particles;
    
    //initialize output table
    vector<vector<double>> data_t_n_1 = zero_2d_arr(N,7);

    //initialize predicted table
    vector<vector<double>> data_p_t_n_1 = zero_2d_arr(N,7);
    
    //Prepare Data: Extract last N Rows
    if (table.size() < N) {
        throw std::out_of_range("Table size is smaller than nr_particles");
    }
    vector<vector<double>> data_t_n(table.end() - N, table.end());

    //initialize all needed quantities at t=t_n
    vector<vector<double>> r_n;
    vector<vector<double>> v_n;
    vector<vector<double>> a_n;
    vector<vector<double>> j_n; //j for jerk

    //extract r_n
    for (vector<double> particle : data_t_n) {
        r_n.push_back(extract_position(particle));
    }
    //extract v_n
    for (vector<double> particle : data_t_n) {
        v_n.push_back(extract_velocity(particle));
    }
    //calculate a_n, j_n
    a_n = acceleration(data_t_n);
    j_n = jerk(data_t_n);


    //initialize all quantities to be calculated, t=n+1
    vector<vector<double>> rp_n_1;
    vector<vector<double>> vp_n_1;
    vector<vector<double>> ap_n_1;
    vector<vector<double>> jp_n_1;

    //calculate vp_n_1
    for (int i = 0; i<N; i++) {
        vector<double> new_vel_p = {0,0,0};

        new_vel_p = v_n[i] + delta_t * a_n[i] + 1.0/2 * (delta_t * delta_t)*j_n[i];

        vp_n_1.push_back(new_vel_p);
    }

    //calculate rp_n_1
    for (int i = 0; i<N; i++) {
        vector<double> new_pos_p = {0,0,0};

        new_pos_p = r_n[i] + delta_t * v_n[i] + 1.0/2 * (delta_t * delta_t)*a_n[i] + 1.0/6*(delta_t*delta_t*delta_t)*j_n[i];

        rp_n_1.push_back(new_pos_p);
    }

    //push rp_n_1 and masses to output in order to calculate ap_n+1
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<3; j++) {
            data_p_t_n_1[i][j] = rp_n_1[i][j];
        }
        data_p_t_n_1[i][6] = data_t_n[i][6];
    }

    //calculate ap_n+1
    ap_n_1 = acceleration(data_p_t_n_1);

    //push vp_n_1 to output in order to calculate jp_n+1
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<3; j++) {
            data_p_t_n_1[i][j+3] = vp_n_1[i][j];
        }
    }

    //calculate jp_n+1
    jp_n_1 = jerk(data_p_t_n_1);

    //initialize second and third derivative of acceleration a2_n, a3_n
    vector<vector<double>> a2_n;
    vector<vector<double>> a3_n;

    //calculate a2_n
    for (int i = 0; i<N; i++) {
        vector<double> new_acc = {0,0,0};

        new_acc = -6*((1/(delta_t*delta_t)*(a_n[i]-ap_n_1[i]))) - 2*(1/delta_t) * (2*j_n[i]+jp_n_1[i]);

        a2_n.push_back(new_acc);
    }

    //calculate a3_n
    for (int i = 0; i<N; i++) {
        vector<double> new_jerk = {0,0,0};

        new_jerk = 12*((1/(delta_t*delta_t*delta_t)*(a_n[i]-ap_n_1[i]))) + 6*(1/(delta_t*delta_t)) * (j_n[i]+jp_n_1[i]);

        a3_n.push_back(new_jerk);
    }

    //initialize corrected values
    vector<vector<double>> rc_n_1;
    vector<vector<double>> vc_n_1;

    //calculate vc_n_1
    for (int i = 0; i<N; i++) {
        vector<double> new_vel_c = {0,0,0};

        new_vel_c = vp_n_1[i] + 1.0/6*pow(delta_t,3) * a2_n[i] + 1.0/24 *pow(delta_t,4)*a3_n[i];

        vc_n_1.push_back(new_vel_c);
    }

    //calculate rc_n_1
    for (int i = 0; i<N; i++) {
        vector<double> new_pos_c = {0,0,0};

        new_pos_c = rp_n_1[i] + 1.0/24*pow(delta_t,4) * a2_n[i] + 1.0/120*pow(delta_t,5)*a3_n[i];

        rc_n_1.push_back(new_pos_c);
    }

    

    //push rc_n_1 and masses to output
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<3; j++) {
            data_t_n_1[i][j] = rc_n_1[i][j];
        }
        data_t_n_1[i][6] = data_t_n[i][6];
    }

    //push vc_n_1 to output
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<3; j++) {
            data_t_n_1[i][j+3] = vc_n_1[i][j];
        }
    }

    return data_t_n_1;
}