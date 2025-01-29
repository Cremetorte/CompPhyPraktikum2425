#include <iostream>
#include <vector>
#include <stdexcept>
#include <random>
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <cmath>
#include "lib/functions.hpp"

using namespace std;

// Lattice width W
int M = 64;

// Rod length L
int L = 8;

// Zustandssume Z
double Z = 0.1;

// Iteration steps
long int totIt = 4*pow(10,9);

vector<vector<int>> horList;
vector<vector<int>> verList;
vector<vector<int>> occField(M, vector<int>(M, 0));  // OccField[i][j]; like matrix notation

random_device rd;  
mt19937 gen(rd());

int periodicIndex(int index) {
    return (index % M + M) % M; // Handles negative indices as well
}

bool overlap(int i, int j, bool vertical) {
    if (vertical) {
        int y;
        for (int dy=0; dy<L; dy++) {
            y = periodicIndex(i - dy);
            if (occField[y][j] != 0) {
                return true;
            }
        }
        return false;
    }
    else {
        int x;
        for (int dx=0; dx<L; dx++) {
            x = periodicIndex(i + dx);
            if (occField[i][x] != 0) {
                return true;
            }
        }
        return false;
    }
}

void addRod(int pos_M, int pos_N, bool vertical) {
    if (!overlap(pos_M,pos_N,vertical)) {
        vector<int> pos = {pos_M,pos_N};
        
        if (vertical) {
            // add to vertical rod list
            verList.push_back(pos);

            // add to Occupation Field
            int y;
            for (int dy=0; dy<L; dy++) {
                y = periodicIndex(pos_M - dy);
                occField[y][pos_N] = 1;
            }

        }
        else {
            // add to horzontal rod list
            horList.push_back(pos);

            // add to Occupation Field
            // int x_p;
            // for (int x=N; x<N+L; x++){
            //     x_p = periodicIndex(x);
            //     occField[M][x_p] = 1;
            // }
            int x;
            for (int dx=0; dx<L; dx++) {
                x = periodicIndex(pos_N + dx);
                occField[pos_M][x] = 1;
            }
        }
    } 
    else {
        throw invalid_argument("Rods would intersect!");
    }
}

bool delRod(int id, bool vertical) {
    if (vertical) {
        if (id < 0 || id >= verList.size()) {
            throw invalid_argument("Id is not in verList");
        }
        int m = verList[id][0];
        int n = verList[id][1];

        // delete from Occupation Field
        int y;
        for (int dy = 0; dy < L; dy++) {
            y = periodicIndex(m - dy);
            occField[y][n] = 0;
        }

        // remove from vertical List
        verList.erase(verList.begin() + id);
        return true;
    } else {
        if (id < 0 || id >= horList.size()) {
            throw invalid_argument("Id is not in horList");
        }
        int m = horList[id][0];
        int n = horList[id][1];

        // remove from horizontal list
        horList.erase(horList.begin() + id);

        // delete from Occupation Field
        int x;
        for (int dx = 0; dx < L; dx++) {
            x = periodicIndex(n + dx);
            occField[m][x] = 0;
        }

        return true;
    }
    return false;
}


int N() {
    return horList.size() + verList.size();
}

int randomInt(int lower_bound, int upper_bound) {
    uniform_int_distribution<> dis(lower_bound, upper_bound);

    int res = dis(gen);

    return res;
}

double randomDouble(double lower_bound, double upper_bound) { 
    uniform_real_distribution<> dis(lower_bound, upper_bound);

    double res = dis(gen);

    return res;
}

void addRandomRod() {
    int m = randomInt(0, M-1);
    int n = randomInt(0, M-1);

    bool vertical = randomInt(0,1);

    if (!overlap(m,n,vertical)) {
        addRod(m, n, vertical);
    }    
}

void deleteRandomRod() {
    int id = randomInt(0, N()-1);
    if (id < horList.size()) {
        delRod(id, false);
    } else {
        delRod(id - horList.size(), true);
    }
}

void gcmcStep() {
    if (randomInt(0,1) == 0) {
        double alpha_ins = 2.0 * M * M / (N() + 1.0) * Z;
        if (randomDouble(0,1) <= alpha_ins) {
            addRandomRod();
        }
    }
    else {
        double alpha_del = 1.0*N()/2/pow(M,2) * 1.0/Z;
        if (randomDouble(0,1) <= alpha_del) {
            deleteRandomRod();
        }
    }
}


int main(/*int argc, char* argv[]*/) {
    
    // if (argc != 6) {
    //     cout << "Wrong number of arguments! Usage: " << argv[0] << " integrator N delta_t t_max video?" << endl;
    //     return -1;
    // }


    vector<int> totalRods;
    vector<int> diffRods;
    vector<int> horRods;
    vector<int> verRods;

    cout << "Beginning calculation for z=" << Z << ", doing " << totIt << " iterations." << endl;

    // Startzeit
    auto start = chrono::high_resolution_clock::now();
    
    for (long int it = 1; it<totIt; it++) {
        
        gcmcStep();

        if (it%100 == 0) {
            totalRods.push_back(N());
            diffRods.push_back(horList.size() - verList.size());
            horRods.push_back(horList.size());
            verRods.push_back(verList.size());
        }
        if (it%1000000 == 0){
            auto ittime = chrono::high_resolution_clock::now();
            auto duration = chrono::duration_cast<std::chrono::seconds>(ittime - start);

            int el_minutes = duration.count() / 60;
            int el_seconds = duration.count() % 60;


            long int est_time = static_cast<long int>(duration.count()) *  totIt / it;

            int est_minutes = est_time / 60;
            int est_seconds = est_time % 60;

            cout << "\rCalculated " << fixed << setprecision(2) << setw(5) << (double)it/totIt*100.0 << "% of all steps. ";
            cout << "Elapsed/Estimated time [min:s]: " << el_minutes << ":" << setw(2) << setfill('0') << el_seconds;
            cout << "/" << est_minutes << ":" << setw(2) << setfill('0') << setprecision(2) << est_seconds << "      ";
        }

    }
    cout << "\nfinished calculation";
    exportIntVecCSV(totalRods, "Output/TotalRods.csv");
    exportIntVecCSV(diffRods, "Output/diffRods.csv");
    exportIntVecCSV(horRods, "Output/horRods.csv");
    exportIntVecCSV(verRods, "Output/verRods.csv");


    // printMatrix(occField);

    // addRod(2,2, true);

    // printMatrix(occField);

    // delRod(0, true);

    // printMatrix(occField);
 
    // int nr_ones = 0;
    // int nr_zeros = 0;
    // for (long int i=0; i<500000000; i++) {
    //     if (randomInt(0,1) == 1) {
    //         nr_ones++;
    //     }
    //     else {
    //         nr_zeros++;
    //     }
    // }

    // cout << "Ones: " << nr_ones << endl;
    // cout << "Zeros: " << nr_zeros << endl;
    // cout << "Est. prob of one: " << (double)nr_ones/(nr_ones+nr_zeros) << endl;




    return 0;
}