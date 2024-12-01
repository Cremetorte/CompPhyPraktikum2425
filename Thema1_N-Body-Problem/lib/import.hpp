#ifndef IMPORT_HPP
#define IMPORT_HPP

#include <vector>
#include <string>

using namespace std;

// declare the functions here
vector<vector<double>> importData(const string& filename);
void print_data(vector<vector<double>> data);
vector<vector<double>> process_data(vector<vector<double>> importedData); 

#endif
