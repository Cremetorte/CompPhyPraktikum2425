#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "import.hpp"

using namespace std;

vector<vector<double>> velocity_verlet_V2(vector<vector<double>> table, double delta_t, int nr_Particles) {
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
 
    //extract r_n
    for (vector<double> particle : data_t_n) {
        r_n.push_back(extract_position(particle));
    }
    //extract v_n
    for (vector<double> particle : data_t_n) {
        v_n.push_back(extract_velocity(particle));
    }
    //calculate a_n
    a_n = acceleration(data_t_n);


    //initialize all quantities to be calculated, t=n+1
    vector<vector<double>> r_n_1;
    vector<vector<double>> v_n_1;
    vector<vector<double>> a_n_1;

    //calculate r_n_1
    for (int i = 0; i<N; i++) {
        vector<double> new_pos = {0,0,0};

        vector<double> v_part = scalar_multiplication(delta_t, v_n[i]);
        vector<double> a_part = scalar_multiplication(0.5*delta_t*delta_t, a_n[i]);
        new_pos = add_vectors(r_n[i], new_pos);
        new_pos = add_vectors(v_part, new_pos);
        new_pos = add_vectors(a_part, new_pos);

        r_n_1.push_back(new_pos);
    }

    //push r_n_1 and masses to output in order to calculate a_n+1
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<3; j++) {
            data_t_n_1[i][j] = r_n_1[i][j];
        }
        data_t_n_1[i][6] = data_t_n[i][6];
    }

    //calculate a_n+1
    a_n_1 = acceleration(data_t_n_1);

    //calculate v_n_1
    for (int i = 0; i<N; i++) {
        vector<double> new_vel = {0,0,0};

        vector<double> v_part = v_n[i];
        vector<double> sum_acc = add_vectors(a_n[i],a_n_1[i]);
        sum_acc = scalar_multiplication(0.5*delta_t,sum_acc);
        new_vel = add_vectors(v_part, sum_acc);

        /* cout << "New Velocity of Particle " << i << ":";
        print_Vector(new_vel);
 */
        v_n_1.push_back(new_vel);
    }

    //push v_n_1 to output
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<3; j++) {
            data_t_n_1[i][j+3] = v_n_1[i][j];
        }
    }

    return data_t_n_1;

}