#ifndef EXPORT_HPP 
#define EXPORT_HPP

#include "import.hpp"
#include "functions.hpp"
#include "export.cpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;


// declare the functions here
void write_to_csv(vector<vector<double>> data, const string& path_filename);



#endif