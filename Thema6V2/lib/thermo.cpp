#include <vector>
#include <stdexcept>
#include <algorithm>
#include <iostream>
#include "randGen.hpp"
#include "thermo.hpp"

using namespace std;

int L = 8;

int periodicIndex(const int& index, const int& M) {
    return (index % M + M) % M; 
}

bool overlap(const int& i, const int& j, const bool& vertical, int (&occField)[lat_Points][lat_Points]) {
    int M = lat_Points;

    if (vertical) { // vertical rod
        int y;
        for (int dy = 0; dy < L; dy++) {
            y = periodicIndex(j + dy, M); // use periodic indices
            if (occField[i][y] != 0) {
                return true;
            }
        }
        return false;
    } else { // horizontal rod
        int x;
        for (int dx = 0; dx < L; dx++) {
            x = periodicIndex(i + dx, M); // use periodic indices
            if (occField[x][j] != 0) {
                return true;
            }
        }
        return false;
    }
}

bool addRod(const int& x, const int& y, const bool& vertical, vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]) {
    int M = lat_Points;
    
    vector<int> pos = {x, y};

    if (overlap(x, y, vertical, occField)) {
        return false;
    }
    
    if (vertical) {
        // add to vertical rod list
        verList.push_back(pos);

        // update occupation field
        int m;
        for (int dy = 0; dy < L; dy++) {
            m = periodicIndex(y + dy, M);
            occField[x][m] = 1;
        }
        
    } else {
        // add to horizontal rod list
        horList.push_back(pos);

        // update occupation field
        int n;
        for (int dx = 0; dx < L; dx++) {
            n = periodicIndex(x + dx, M);
            occField[n][y] = 1;
        }
    }
    return true;
}

bool addRandomRod(vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]) {
    int M = lat_Points;

    // choose random orientation
    bool rotation = randomInt(0, 1) == 1;

    // choose random position
    int x = randomInt(0, M - 1);
    int y = randomInt(0, M - 1);

    return addRod(x, y, rotation, horList, verList, occField);
}

void delRod(int id, vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]) {
    int M = lat_Points;

    int n_hor = horList.size();
    int n_ver = verList.size();

    if (n_hor == 0 && n_ver == 0) { // check if there are any rods
        return;
    }
        
    if (id < 0 || id > n_hor + n_ver - 1) { // check if ID is in range
        throw invalid_argument("Rod with given ID doesn't exist!");
    }

    if (id < horList.size()) { // delete horizontal rod
        // get position
        int x = horList[id][0];
        int y = horList[id][1];

        // delete from list
        horList.erase(horList.begin() + id);

        // update occupation field
        int n;
        for (int dx = 0; dx < L; dx++) {
            n = periodicIndex(x + dx, M);
            occField[n][y] = 0;
        }    

    } else { // delete vertical rod
        // get index of vertical rod
        id = id - horList.size();

        // get position
        int x = verList[id][0];
        int y = verList[id][1];

        // delete from list
        verList.erase(verList.begin() + id);

        // update occupation field
        int m;
        for (int dy = 0; dy < L; dy++) {
            m = periodicIndex(y + dy, M);
            occField[x][m] = 0;
        } 
    }
}

void delRandomRod(vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]) {
    int n_hor = horList.size();
    int n_ver = verList.size();

    if (n_hor == 0 && n_ver == 0) { // check if there are any rods
        return;
    }

    // choose random rod
    int randID = randomInt(0, n_hor + n_ver - 1);
    // delete rod
    delRod(randID, horList, verList, occField);
}

bool gcmcStep(vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points], const double& Z) {
    int M = lat_Points;

    int n_hor = horList.size();
    int n_ver = verList.size();
    int N = n_hor + n_ver;
    
    if (randomInt(0, 1) == 0) { // add rod
        double alpha_ins = 2.0 * M * M / (N + 1) * Z; // probability for adding a rod

        if (randomDouble(0, 1) < alpha_ins) { // try to add rod
            return addRandomRod(horList, verList, occField);
        } else {
            return false;
        }
    } else {
        double alpha_del = 1.0 * N / (2.0 * M * M) * 1 / Z; // probability for deleting a rod
        if (randomDouble(0, 1) < alpha_del) { // delete rod
            delRandomRod(horList, verList, occField);
            return true;
        } else {
            return false;
        }
    }
}

vector<double> observables(vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]) {
    int M = lat_Points;
    int n_hor = horList.size();
    int n_ver = verList.size();
    int n_tot = n_hor + n_ver;
    double eta = 1.0 * L * n_tot / (M * M);
    double s = 1.0 * (n_hor - n_ver) / n_tot;

    vector<double> res = {(double)n_hor, (double)n_ver, (double)n_tot, eta, s};
    return res;
}