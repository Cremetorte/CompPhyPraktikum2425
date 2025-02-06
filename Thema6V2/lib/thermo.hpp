#ifndef THERMO_HPP
#define THERMO_HPP


// Include Libraries here
#include <vector>

using namespace std;

const int lat_Points = 64; // Define as a constant expression

// Declare Functions here
int periodicIndex(const int& index, const int& M);
bool overlap(const int& i, const int& j, const bool& vertical, int (&occField)[lat_Points][lat_Points]);
bool addRod(const int& x, const int& y, const bool& vertical, vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]);
bool addRandomRod(vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]);
void delRod(int id, vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]);
void delRandomRod(vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]);
bool gcmcStep(vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points], const double& Z);
vector<double> observables(vector<vector<int>>& horList, vector<vector<int>>& verList, int (&occField)[lat_Points][lat_Points]);

#endif // THERMO_HPP