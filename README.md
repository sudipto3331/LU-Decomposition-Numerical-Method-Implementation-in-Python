# LU Decomposition Numerical Method Implementation in Python

This repository contains a Python implementation of the LU Decomposition method for solving systems of linear equations. The code reads coefficients from an Excel file (`read.xls`), performs LU Decomposition to factorize the matrix into lower and upper triangular matrices, and then solves the system of equations. The method also includes result verification.

## Table of Contents
- [LU Decomposition Theory](#lu-decomposition-theory)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Example](#example)
- [Files in the Repository](#files-in-the-repository)
- [Input Parameters](#input-parameters)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

## LU Decomposition Theory
LU Decomposition is an algorithm to decompose a matrix into the product of a lower triangular matrix \(L\) and an upper triangular matrix \(U\). It is used to solve systems of linear equations, invert matrices, and compute determinants.

**Steps:**
1. Decompose the matrix \(A\) into \(L\) and \(U\) such that \(A = LU\).
2. Solve \(LY = B\) for \(Y\) using forward substitution.
3. Solve \(UX = Y\) for \(X\) using back substitution.

## Dependencies
To run this code, you need the following libraries:
- `numpy`
- `xlrd`

## Installation
To install the required libraries, you can use `pip`:
```sh
pip install numpy xlrd
```

## Usage
1. Clone the repository.
2. Ensure the script and the Excel file (`read.xls`) are in the same directory.
3. Run the script using Python:
    ```sh
    python lu_decomposition.py
    ```

## Code Explanation
The code begins by importing the necessary libraries and reading the matrix of coefficients and constants from the Excel file. It then performs LU Decomposition to factorize the matrix into lower and upper triangular matrices. Finally, it solves the system of equations using forward and backward substitution and verifies the results.

Below is a snippet from the code illustrating the main logic:

```python
import numpy as np
import xlrd

# Reading data from excel file
loc = ('read.xls')
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

n = sheet.nrows
a = np.zeros([n, n+1])
b = np.zeros([n, n+1])
B = np.zeros([n-1, n, n+1])
U = np.zeros([n, n+1])
L = np.zeros([n, n])
X = np.zeros([n])
d = np.zeros([n])
p = np.zeros([n])

for i in range(sheet.ncols):
    for j in range(sheet.nrows):
        a[j, i] = sheet.cell_value(j, i)

for i in range(n):
    for j in range(n+1):
        if i == 0:
            b[i, j] = a[i, j]
        if i > 0:
            b[i, j] = a[i, j] - (a[0, j] * (a[i, 0] / a[0, 0]))

if n < 3:
    U = b[:, :-1]
else:
    B[0, :, :] = b
    for k in range(n-2):
        for i in range(n):
            for j in range(n+1):
                if all([i > k+1, j < k+1]):
                    B[k+1, i, j] = B[k, i, j] - (B[k, k, j] * (B[k, i, k] / B[k, k, k]))
                if all([i > k+1, j > k]):
                     B[k+1, i, j] = B[k, i, j] - (B[k, k+1, j] * (B[k, i, k+1] / B[k, k+1, k+1]))
                if i < k+2:
                    B[k+1, i, j] = B[k, i, j]
    U = B[k+1, :, :-1]

print('The upper triangle matrix is:')
print(U)

# Lower triangle matrix generation    
for j in range(n):
    for i in range(n):
        if i == j:
            L[i, j] = 1
        if j < i:
            if j == 0:
                L[i, j] = a[i, j] / a[j, j]
            if j > 0:
                L[i, j] = B[j-1, i, j] / B[j-1, j, j]

print('The lower triangle matrix is:')
print(L)

# Solve LY = B
d[0] = a[0, n] / L[0, 0]
for i in range(1, n):
    summation = 0
    for k in range(n):
        summation += L[i, k] * d[k]
    d[i] = (a[i, n] - summation) / L[i, i]

print('The right hand side matrix is:')
print(d)

# Solve UX = Y
X[n-1] = d[n-1] / U[n-1, n-1]
for i in range(n-2, -1, -1):
    summation = 0
    for k in range(i+1, n):
        summation += U[i, k] * X[k]
    X[i] = (d[i] - summation) / U[i, i]

print('The values of the unknown variables are respectively:')
print(X)

# Result Verification    
for i in range(n):
    summation = 0
    for j in range(n):
        summation += a[i, j] * X[j]
    p[i] = summation - a[i, j+1]

print('The verification results are:')
print(p)
print('The implementation is correct if verification results are all zero')
```

The code completes by verifying the results and printing them to the console.

## Example
Below is an example of how to use the script:

1. Prepare the `read.xls` file with the system of equations in matrix form.
2. **Run the script**:
    ```sh
    python lu_decomposition.py
    ```

3. **Output**:
    - The script will compute the results using the LU Decomposition method and print the upper triangular matrix, lower triangular matrix, right-hand side matrix, values of unknown variables, and verification results to the console.

## Files in the Repository
- `lu_decomposition.py`: The main script for performing the LU Decomposition method.
- `read.xls`: Excel file from which the matrix data is read.

## Input Parameters
The initial input data is expected to be in the form of a matrix within the `read.xls` file. Each row represents coefficients of the variables in the equations, along with the constants.

## Troubleshooting
1. **Excel File**: Ensure that the input matrix is correct and placed in the `read.xls` file.
2. **Matrix Format**: Confirm that the matrix is complete and correctly formatted.
3. **Excel File Creation**: Ensure you have read permissions in the directory where the script is run to load the Excel file.
4. **Python Version**: This script is compatible with Python 3. Ensure you have Python 3 installed.

## Author
Script created by Sudipto.

---

This documentation should guide you through understanding, installing, and using the LU Decomposition method script. For further issues or feature requests, please open an issue in the repository on GitHub. Feel free to contribute by creating issues and submitting pull requests. Happy coding!
