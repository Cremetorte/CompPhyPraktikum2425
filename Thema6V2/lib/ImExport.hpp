#ifndef IMEXPORT_HPP
#define IMEXPORT_HPP


// Include Libraries here
#include <vector>
#include <string>

using namespace std;


// Declare Functions here
template <typename T> void exportVecCSV(const vector<T>& vec, const string& path_filename);
void exportObservablesToCSV(const vector<vector<double>>& matrix, const string& filename);
void printMatrix(const vector<vector<int>>& matrix);

#endif // IMEXPORT_HPP