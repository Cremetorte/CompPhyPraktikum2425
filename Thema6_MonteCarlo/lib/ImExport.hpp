#ifndef IMEXPORT_HPP
#define IMEXPORT_HPP


// Include Libraries here
#include <vector>
#include <string>

using namespace std;


// Declare Functions here
void exportIntVecCSV(const vector<int>& vec, const string& path_filename);
void exportObservablesToCSV(const vector<vector<double>>& matrix, const string& filename);
void exportMatrixToCSV(const vector<vector<int>>& matrix, const string& filename);
void printMatrix(const vector<vector<int>>& matrix);
void print2dArray(int matrix[64][64]);

#endif // IMEXPORT_HPP