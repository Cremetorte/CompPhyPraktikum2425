#include <iostream>
#include <vector>
#include <stdexcept>
#include <random>
#include <algorithm>
#include "lib/functions.hpp"

using namespace std;

// Lattice width W
int M = 5;

// Rod length L
int L = 3;

// Zustandssume Z
double Z = 1;

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
            horList.push_back(pos);

            // add to Occupation Field
            int y;
            for (int dy=0; dy<L; dy++) {
                y = periodicIndex(M - dy);
                occField[y][N] = 1;
            }

        }
        else {
            // add to vertical rod list
            verList.push_back(pos);

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

int randomDouble(double lower_bound, double upper_bound) {
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
            if (overlap(x,y,false)) {
                return false;
            }
            else {
                // create horizontal rod
                double alpha_ins = min(1,2*(double)M*M/(N()+1)*Z);
                double prob_ins = randomDouble(0,1)

                if (prob_ins)
            }
            

        }
    }
    else { 
        // Delete Rod

    }
}


int main(/*int argc, char* argv[]*/) {
    
    // if (argc != 6) {
    //     cout << "Wrong number of arguments! Usage: " << argv[0] << " integrator N delta_t t_max video?" << endl;
    //     return -1;
    // }

    

 


    return 0;
}