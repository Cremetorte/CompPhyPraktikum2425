#include <vector>
#include "functions.hpp"
#include "beschleunigung.hpp"
#include "import.hpp"

using namespace std;

vector<vector<double>> velocity_verlet_V2(vector<vector<double>> table, double delta_t, int nr_Particles) {
    //Prepare Data
    //Extract last N Rows
    int N = nr_Particles;
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
        v_n.push_back(extract_position(particle));
    }
    //calculate a_n
    a_n = acceleration(data_t_n);


    //initialize all quantities to be calculated, t=n+1
    vector<vector<double>> r_n_1;
    vector<vector<double>> v_n_1;
    vector<vector<double>> a_n_1;

    //calculate r_n_1
    for (int i = 0; i<N; i++) {
        

    }


}