#ifndef IMPORT_HPP
#define IMPORT_HPP

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include "import.cpp"


// declare the functions here
std::vector<std::vector<double>> importData(const std::string& filename);
void printData(std::vector<std::vector<double>> data);

#endif