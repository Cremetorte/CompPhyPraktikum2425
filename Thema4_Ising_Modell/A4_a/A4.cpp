#include <iostream>
#include <vector>
#include <random>
#include <fstream>
#include <tuple>
#include <iostream>
#include <cmath>

using namespace std;

using namespace std;

#define L 128                  // Seitenlänge des Gitters
#define N_BETA 100             // Anzahl der beta-Werte
#define NR_OBS 200             // Anzahl der Messungen pro beta
#define N_TRY 5                // Anzahl der Versuche pro Spin bei jedem Update
#define N_THERMALIZING 3000    // Anzahl der Updates zur Thermalisation
#define N_A 1000                // Anzahl der Updates zwischen den Messungen (Dekorrelation)
#define J 1.0                  // Kopplungskonstante
#define h 0.0                  // externes Magnetfeld
#define STEP_SIZE 0.025          // Schrittweite für beta

vector<double> range_vector(double start, double end, double step) {
    vector<double> result;
    for (double value = start; value < end; value += step) {
        result.push_back(value);
    }
    return result;
}

double mean(const vector<double>& data) {
    if (data.empty()) return 0.0;  // Avoid division by zero
    return accumulate(data.begin(), data.end(), 0.0) / data.size();
}

double variance(const vector<double>& data, double beta) {
    if (data.empty()) return 0.0;  // Avoid division by zero

    double avg = mean(data);
    double sum_squared_diff = 0.0;

    for (double value : data) {
        sum_squared_diff += (value - avg) * (value - avg);
    }

    return sum_squared_diff / data.size() * beta * beta;  // Use N (population variance)
}

int** initialize_lattice() {
    int** lattice = new int*[L];
    for (int i = 0; i < L; ++i) {
        lattice[i] = new int[L];
    }

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> dist(0, 1);

    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < L; ++j) {
            lattice[i][j] = (dist(gen) == 0) ? -1 : 1;
        }
    }
    return lattice;
}


// Function to free dynamically allocated memory
void delete_lattice(int** lattice) {
    for (int i = 0; i < L; ++i) {
        delete[] lattice[i];
    }
    delete[] lattice;
}


double hamiltonian(int** spins) {
    double H_spin_coupling = 0;
    double H_ext_mag = 0;

    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < L; ++j) {
            double neighbors_sum = (spins[(i - 1 + L) % L][j] 
                                  + spins[(i + 1) % L][j] 
                                  + spins[i][(j - 1 + L) % L] 
                                  + spins[i][(j + 1) % L]) / 2.0;

            H_spin_coupling -= J * neighbors_sum * spins[i][j];
            H_ext_mag += h * spins[i][j];
        }
    }

    return H_spin_coupling + H_ext_mag;
}


double dH(int s, int s_prime, int i, int j, int** spins) {
    // Sum of neighboring spins (with periodic boundary conditions)
    int neighbors_sum = spins[(i - 1 + L) % L][j] 
                      + spins[(i + 1) % L][j] 
                      + spins[i][(j - 1 + L) % L] 
                      + spins[i][(j + 1) % L];

    // Energy difference between s and s_prime
    double H_s = -J * neighbors_sum * s + h * s;
    double H_s_prime = -J * neighbors_sum * s_prime + h * s_prime;

    return H_s_prime - H_s;
}



void multihit(int** spins, double beta) {
    // random_device rd;
    // mt19937 gen(rd());
    // uniform_int_distribution<int> dist(0, 1);  // Generates 0 or 1
    // uniform_real_distribution<double> rand_prob(0.0, 1.0);  // Generates random double between 0 and 1

    // for (int i = 0; i < L; ++i) {
    //     for (int j = 0; j < L; ++j) {
    //         for (int t = 0; t < N_TRY; ++t) {
    //             int s1 = (dist(gen) == 0) ? -1 : 1;  // Randomly pick -1 or 1
    //             int s = spins[i][j];
                
    //             double change_H = dH(s, s1, i, j, spins);

    //             if (change_H < 0) {
    //                 spins[i][j] = s1;  // Accept new spin
    //             } else {
    //                 double r = rand_prob(gen);
    //                 if (r < exp(-beta * change_H)) {
    //                     spins[i][j] = s1;  // Accept with probability exp(-beta * ΔH)
    //                 }
    //             }
    //         }
    //     }
    // }
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> dist(0, 1);  // Generates 0 or 1
    uniform_real_distribution<double> rand_prob(0.0, 1.0);  // Generates random double between 0 and 1

    

    for (int i=0;i<L;i++) {
        for (int j=0;j<L;j++) {
            int neighbors_sum = spins[(i - 1 + L) % L][j] 
                              + spins[(i + 1) % L][j] 
                              + spins[i][(j - 1 + L) % L] 
                              + spins[i][(j + 1) % L];
            double k = beta * (J * neighbors_sum + h);
            double q = exp(-k)/(2*cosh(k));
            double r = rand_prob(gen);
            spins[i][j] = (rand_prob(gen) < q) ? -1 : +1;
        }
    }
}





tuple<double, double, double> compute_observables(int** spins) {
    double M = 0.0;
    
    // Compute magnetization (sum of all spins)
    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < L; ++j) {
            M += spins[i][j];
        }
    }

    // Compute energy using the Hamiltonian function
    double E = hamiltonian(spins);

    // Normalize observables
    double M_sq = (M * M) / (L * L);
    
    return {E / (L * L), abs(M) / (L * L), M_sq / (L * L)};
}



vector<double> run_metropolis(double beta){
    int** spins = initialize_lattice();
    vector<double> energies;
    vector<double> magnetizations;
    vector<double> magnetizations_sq;
    
    double mean_energy = 0.0;
    double mean_magnetization = 0.0;
    double mean_magnetization_sq = 0.0;
    double specific_heat = 0.0;

    // Thermalization
    for (int i = 0; i < N_THERMALIZING; i++) {
        multihit(spins, beta);
    }

    // Measurement
    for (int i = 0; i < NR_OBS; ++i) {
        for (int j = 0; j < (N_A*beta + 10); ++j) {
            multihit(spins, beta);
        }

        auto [E, M, M_sq] = compute_observables(spins);
        energies.push_back(E);
        magnetizations.push_back(M);
        magnetizations_sq.push_back(M_sq);
    }

    mean_energy = mean(energies);
    mean_magnetization = mean(magnetizations);
    mean_magnetization_sq = mean(magnetizations_sq);
    specific_heat = variance(energies, beta);


    delete_lattice(spins);


    return {beta, mean_energy, mean_magnetization, mean_magnetization_sq, specific_heat};
}


int main() {
    vector<double> betas = range_vector(0.01, 1.0, STEP_SIZE);
    vector<vector<double>> results(betas.size());

    cout << "Running simulations for " << betas.size() << " beta values" << endl;

    #pragma omp parallel for
    for (size_t idx = 0; idx < betas.size(); ++idx) {
        double beta = betas[idx];
        cout << "Running simulation for beta = " << beta << endl;
        results[idx] = run_metropolis(beta);
    }

    ofstream file("results.csv");
    file << "beta,mean_energy,mean_magnetization,mean_magnetization_sq,specific_heat\n";

    for (const auto& result : results) {
        for (size_t i = 0; i < result.size(); ++i) {
            file << result[i];
            if (i < result.size() - 1) {
                file << ",";
            }
        }
        file << "\n";
    }

    file.close();
    cout << "Results saved to results.csv" << endl;

    return 1;
}