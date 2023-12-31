# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 10:47:50 2023

@author: Núria
"""




from numpy import ones, real, imag, zeros, loadtxt, absolute, interp, array, linspace, insert, delete, shape, arange, array_equal, random, vstack, transpose, savetxt, flip, concatenate, mean
from math import floor
import csv
import pandas as pd
import os



header=[]
data=[]
ii=0
filename='B068B3_mem_best' #Name of the file
opFile=False;

## Import the file and read it
path1='Y:\Filters and Emitters\Filters\Mapsi_B001_B050\Medidas FTIR JASCO'
path=path1+'\_Raw CSV'
file=open(path+'\\'+filename+'.csv')
type(file)
csvreader=csv.reader(file,delimiter=';')

##Take out all the previous information/rows
while ii<19: #There is information until row 19.
    ii=ii+1
    header=next(csvreader) #store the information in header and position yourself at the start of the data rows

## Store the transmission data
for row in csvreader:
    wl=10000/float(row[0].replace(',','.')) # Replace the decimal coma for a dot and calculate the wavelength
    cc=[wl,float(row[1].replace(',','.'))] #Reconstruct the row
    data.append(cc) # Add the row to the whole data structure
    if floor(float(row[0].replace(',','.')))==5000: #Detect the end of the data and exit the loop, to avoid adding text to the data
        break
file.close()

## Export the data
header=['Wavelength (um)', filename] # Determine the Header of the data
data=pd.DataFrame(data,columns=header) #Store the data to expot in a DataFrame
path=path1+'\\'+filename+'.xlsx'
data.to_excel(path,index=False) #Export the data
if opFile: # You can determine if you want to open the file or not
    os.startfile(path)

