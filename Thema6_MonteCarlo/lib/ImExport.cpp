#include <vector>
#include <iostream>
#include <string>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <limits>
#include "ImExport.hpp"

using namespace std;




/**
 * @brief Exports a vector to a CSV file.
 * 
 * This function takes a vector of elements and writes its contents to a CSV file.
 * Each element of the vector is written to the file, separated by commas.
 * 
 * @tparam T The type of elements in the vector.
 * @param vec The vector to be exported.
 * @param path_filename The path and filename of the CSV file to write to.
 * 
 * @note If the file cannot be opened, an error message is printed to the standard error stream.
 */
void exportIntVecCSV(const vector<int>& vec, const string& path_filename) {
    cout << "\nAttempting to write to " << path_filename << "..." << endl;
    ofstream outputFile(path_filename);

    if (!outputFile.is_open()) {
        cerr << "Error: Could not open file " << path_filename << endl;
        return;
    }

    stringstream line;
    line.str("");
    for (size_t i = 0; i < vec.size(); i++) {
        line << vec[i];
        if (i != vec.size() - 1) {
            line << ",";
        }
    }
    outputFile << line.str();

    outputFile.close();

    cout << "Finished writing CSV." << endl;
}



/**
 * @brief Exports a matrix of observables to a CSV file.
 *
 * This function takes a matrix of observables and writes it to a CSV file with a specified filename.
 * The first row of the CSV file contains the header: "n_hor,n_ver,n_tot,eta,S".
 * Each subsequent row contains the data from the matrix, with each element separated by a comma.
 *
 * @param matrix A vector of vectors containing the observables to be exported.
 * @param filename The name of the file to which the data will be exported.
 */
void exportObservablesToCSV(const vector<vector<double>>& matrix, const string& filename) {
    cout << "Attemtring to write to " << filename << "..." << endl;
    ofstream outputFile(filename);
    

    if (!outputFile.is_open()) {
        cerr << "Error: Could not open file " << filename << endl;
        return;
    }

    stringstream line;

    // add header row
    line.str("");
    line << "n_hor,n_ver,n_tot,eta,S\n";
    outputFile << line.str();

    // add data rows
    for (vector<double> row : matrix) {
        line.str("");
        for (int i = 0; i < row.size()-1; i++) {
            line << setprecision(8) << row[i];
            line << ",";
        }
        line << setprecision(8) << row[row.size()-1] << "\n";
        outputFile << line.str();
    }

    outputFile.close();

    cout << "Finished writing CSV." << endl;

}



/**
 * @brief Exports a matrix to a CSV file.
 *
 * This function takes a 2D vector (matrix) of integers and writes its contents
 * to a CSV file specified by the filename. Each row of the matrix is written
 * as a line in the CSV file, with elements separated by commas.
 *
 * @param matrix The 2D vector of integers to be exported.
 * @param filename The name of the CSV file to write to.
 */
void exportMatrixToCSV(const vector<vector<int>>& matrix, const string& filename) {
    cout << "Attemtring to write to " << filename << "..." << endl;
    ofstream outputFile(filename);
    

    if (!outputFile.is_open()) {
        cerr << "Error: Could not open file " << filename << endl;
        return;
    }

    stringstream line;

    // add data rows
    for (vector<int> row : matrix) {
        line.str("");
        for (int i = 0; i < row.size()-1; i++) {
            line << row[i];
            line << ",";
        }
        line << setprecision(8) << row[row.size()-1] << "\n";
        outputFile << line.str();
    }

    outputFile.close();

    cout << "Finished writing CSV." << endl;

}



/**
 * @brief Prints a 2D matrix to the standard output.
 * 
 * This function takes a 2D vector (matrix) of integers and prints its elements
 * in a tab-separated format. Each row of the matrix is printed on a new line.
 * 
 * @param matrix A constant reference to a 2D vector of integers representing the matrix to be printed.
 */
void printMatrix(const vector<vector<int>>& matrix) {
    for (int i=0; i<matrix.size(); i++) {
        for (int j=0; j<matrix[0].size(); j++) {
            cout << matrix[i][j];
        }
        cout << "\n";
    }
}


void print2dArray(int matrix[64][64]) {
    for (int i=0; i<64; i++) {
        for (int j=0; j<64; j++) {
            cout << matrix[i][j];
        }
        cout << "\n";
    }
}
