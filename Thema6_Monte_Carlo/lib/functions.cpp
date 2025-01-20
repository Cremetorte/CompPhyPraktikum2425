#include <vector>
#include <iostream>

using namespace std;


// int* indexPeriodic(const vector<vector<int>> &array, const int& x, const int& y) {
//     int i_per = x % array.size();
//     int j_per = y % array[0].size();

//     return &array[i_per][j_per];
// }


// vector<vector<int>> occField(const vector<vector<int>>& hor_list, const vector<vector<int>>& ver_list, const int& M, const int& L){
//     vector<vector<int>> res(M, vector<int>(M, 0));

//     for (vector<int> rod : hor_list){
//         int x_0 = rod[0];
//         int y_0 = rod[1];
//         for (int x=0; x++; x<L) {
//             res[x][y_0] = 1;
//         }
//     }

// }


void printMatrix(const vector<vector<int>>& matrix) {
    for (int i=0; i<matrix.size(); i++) {
        for (int j=0; j<matrix[0].size(); j++) {
            cout << matrix[i][j] << "\t";
        }
        cout << "\n";
    }
}