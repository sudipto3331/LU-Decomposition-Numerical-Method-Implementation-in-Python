# -*- coding: utf-8 -*-
"""

@author: Sudipto
"""

##Import libraries as necessary
import numpy as np
import xlrd 

#Reading data from excel file
loc = ('read.xls')

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

n=sheet.nrows   
a=np.zeros([n,n+1])
b=np.zeros([n,n+1])
B=np.zeros([n-1,n,n+1])
U=np.zeros([n,n+1])
L=np.zeros([n,n])
X=np.zeros([n])
d=np.zeros([n])
p=np.zeros([n])

for i in range(sheet.ncols):
    for j in range(sheet.nrows):
        #print(sheet.cell_value(1, i))
        a[j,i]=sheet.cell_value(j, i)
        
for i in range(n):
    for j in range(n+1):
        if i==0:
            b[i,j]=a[i,j]
        if i>0:
            b[i,j]=a[i,j]-(a[0,j]*(a[i,0]/a[0,0]))
#print(b)            
if n<3:
    U=b[:,:-1]

if n>2:
    B[0,:,:]=b 
        
    for k in range(n-2):
        for i in range(n):
            for j in range(n+1):
                
                if all ([i>k+1, j<k+1]):
                    B[k+1,i,j]=B[k,i,j]-(B[k,k,j]*(B[k,i,k]/B[k,k,k]))
        
                if all ([i>k+1, j>k]):
                     B[k+1,i,j]=B[k,i,j]-(B[k,k+1,j]*(B[k,i,k+1]/B[k,k+1,k+1]))
        
                if i<k+2:
                    B[k+1,i,j]=B[k,i,j]
            
    U=B[k+1,:,:-1] 

print('The upper triangle matrix is:')
print(U)

#Lower triangle matrix generation    
for j in range(n):
    for i in range(n):
        
        if i==j:
            L[i,j]=1
        
        if all([j<i]):
            if j==0:
                L[i,j]=a[i,j]/a[j,j]
            if j>0:
                L[i,j]=B[j-1,i,j]/B[j-1,j,j]

print('The lower triangle matrix is:')
print(L)

#[L][D]=[B]
d[0]=a[0,n]/L[0,0]
for i in range(1,n):
    summation=0
    for k in range(n):
        summation=summation+L[i,k]*d[k]
        
    d[i]=(a[i,n]-summation)/L[i,i]  

print('The right hand side matrix is:')    
print(d)

X[n-1]=d[n-1]/U[n-1,n-1]
for i in range(n-2,-1,-1):
    summation=0
    for k in range(i+1,n):
        summation=summation+U[i,k]*X[k]
        
    X[i]=(d[i]-summation)/U[i,i]  
    
print('The values of the unknown variables are respectively:')
print(X)         

#Result Verification    
for i in range(n):
    summation=0
    for j in range(n):
        summation=summation+a[i,j]*X[j]
    
    p[i]=summation-a[i,j+1]

#The implementation is corrct if verification results are all zero
print('The verification results are:')
print(p)
print('The implementation is corrct if verification results are all zero')         
