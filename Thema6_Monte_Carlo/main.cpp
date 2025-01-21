#include <iostream>
#include <vector>
#include <stdexcept>
#include <random>
#include <algorithm>
#include <chrono>
#include <iomanip>
#include "lib/functions.hpp"

using namespace std;

// Lattice width W
int M = 64;

// Rod length L
int L = 8;

// Zustandssume Z
double Z = 0.56;

// Iteration steps
long int totIt = 10000000;

vector<vector<int>> horList;
vector<vector<int>> verList;
vector<vector<int>> occField(M, vector<int>(M, 0));  // OccField[i][j]; like matrix notation

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

void addRod(int M, int N, bool vertical) {
    if (!overlap(M,N,vertical)) {
        vector<int> pos;
        pos.push_back(M);
        pos.push_back(N);
        if (vertical) {
            // add to horizontal rod list
            verList.push_back(pos);

            // add to Occupation Field
            int y;
            for (int dy=0; dy<L; dy++) {
                y = periodicIndex(M - dy);
                occField[y][N] = 1;
            }

        }
        else {
            // add to vertical rod list
            horList.push_back(pos);

            // add to Occupation Field
            // int x_p;
            // for (int x=N; x<N+L; x++){
            //     x_p = periodicIndex(x);
            //     occField[M][x_p] = 1;
            // }
            int x;
            for (int dx=0; dx<L; dx++) {
                x = periodicIndex(N + dx);
                occField[M][x] = 1;
            }
        }
    } 
    else {
        throw invalid_argument("Rods would intersect!");
    }
}

bool delRod(int id, bool vertical) {
    int m = verList[id][0];
    int n = verList[id][1];

    if (vertical) {
        // delete from Occupation Field
        int y;
        for (int dy=0; dy<L; dy++) {
            y = periodicIndex(m - dy);
            occField[y][n] = 0;
        }

        // remove from vertical List
        verList.erase(verList.begin()+id);
        return true;
    }
    else {
        // remove from horizontal list
        horList.erase(horList.begin()+id);

        // delete from Occupation Field
        int x;
        for (int dx=0; dx<L; dx++) {
            x = periodicIndex(n + dx);
            occField[m][x] = 1;
        }

        return true;
    }
    return false;
}


int N() {
    return horList.size() + verList.size();
}

int randomInt(int lower_bound, int upper_bound) {
    random_device rd;  
    mt19937 gen(rd()); 
    uniform_real_distribution<> dis(lower_bound, upper_bound);

    int res = dis(gen);

    return res;
}

double randomDouble(double lower_bound, double upper_bound) {
    random_device rd;  
    mt19937 gen(rd()); 
    uniform_real_distribution<> dis(lower_bound, upper_bound);

    double res = dis(gen);

    return res;
}

bool gcmcStep() {
    int prob_ins_del = randomInt(0,1);

    if (prob_ins_del == 0) {
        // Insert Rod

        // random Position
        int x = randomInt(0,M-1);
        int y = randomInt(0,M-1);

        double prob_rot = randomInt(0,1);
        if (prob_rot == 0) {
            // Horizontal Rod
            if (overlap(x,y,false)) {
                return false;
            }
            else {
                // create horizontal rod
                double alpha_ins = 2*(double)M*M/(N()+1)*Z;
                alpha_ins = min(1.0, alpha_ins);
                double prob_ins = randomDouble(0,1);

                if (prob_ins < alpha_ins){
                    addRod(x,y, false);
                }
                return true;
            } 
        }
        else{
            // Horizontal Rod
            if (overlap(x,y,true)) {
                return false;
            }
            else {
                // create horizontal rod
                double alpha_ins = 2*(double)M*M/(N()+1)*Z;
                alpha_ins = min(1.0, alpha_ins);
                double prob_ins = randomDouble(0,1);

                if (prob_ins < alpha_ins){
                    addRod(x,y, true);
                }
                return true;
            }
        }
    }
    else { 
        // Delete Rod
        double alpha_del = (double)N()/2/M/M/Z;
        alpha_del = min(1.0, alpha_del);
        if (randomDouble(0,1) < alpha_del){
            int random_rod = randomInt(0, N()-1);
            if (random_rod <= verList.size()) {
                delRod(random_rod, true);
            }
            else {
                delRod(random_rod, false);
            }
            return true;
        }
        else {
            return false;
        }
    }
}

bool gcmcStepGOTO() {
    if (randomDouble(0,1) < 0.5) {
        // delete Rod
        double alpha_del = min(1.0, (double)N()/2/M/M/Z);
        if (randomDouble(0,1) < alpha_del) {
            goto removeRod;
        }
        else {
            return false;
        }
    }
    else {
        //random orientation
        bool vert = (randomDouble(0,1) < 0.5);

        //random Position
        int x = randomInt(0,M-1);      
        int y = randomInt(0,M-1); 

        //check for Collisions
        if (overlap(x,y,vert)) {
            return false;
        }

        //add Rod
        double alpha_ins = min(1.0, 2*(double)M*M/(N()+1)*Z);
        if (randomDouble(0,1) < alpha_ins) {
            addRod(x,y,vert);
            return true;
        }

    }


    removeRod: 
    {
        int r_id = randomInt(0,N());
        if (r_id < horList.size()) {
            delRod(r_id, false);
        }
        else {
            delRod(r_id-horList.size(), true);
        }
        return true;
    }

}




int main(/*int argc, char* argv[]*/) {
    
    // if (argc != 6) {
    //     cout << "Wrong number of arguments! Usage: " << argv[0] << " integrator N delta_t t_max video?" << endl;
    //     return -1;
    // }
    vector<int> totalRods;
    vector<int> diffRods;

    cout << "Beginning calculation for z=" << Z << ", doing " << totIt << " iterations." << endl;

    // Startzeit
    auto start = chrono::high_resolution_clock::now();
    
    for (long int it = 1; it<totIt; it++) {
        
        gcmcStepGOTO();

        if (it%100 == 0) {
            totalRods.push_back(N());
            diffRods.push_back(horList.size() - verList.size());
        }
        if (it%10000 == 0){
            auto ittime = chrono::high_resolution_clock::now();
            auto duration = chrono::duration_cast<std::chrono::seconds>(ittime - start);

            int el_minutes = duration.count() / 60;
            int el_seconds = duration.count() % 60;


            long int est_time = static_cast<long int>(duration.count()) *  totIt / it;

            int est_minutes = est_time / 60;
            int est_seconds = est_time % 60;

            cout << "\rCalculated " << (double)it/totIt*100.0 << "\% of all steps. " 
                << "Elapsed/Estimated time [min:s]: " << el_minutes << ":" << setw(2) << setfill('0') << el_seconds
                << "/" << est_minutes << ":" << setw(2) << setfill('0') << est_seconds;
        }

    }
    cout << "\nfinished calculation";
    exportIntVecCSV(totalRods, "Output/TotalRods.csv");
    exportIntVecCSV(diffRods, "Output/diffRods.csv");

    // addRod(2,2, true);

    // printMatrix(occField);

    // delRod(0, true);

    // printMatrix(occField);
 


    return 0;
}