# =============================================================================
# Mapsi Photonics 
# Simulation Class
# Version PyQt5
# Daniel Segura May 2021
# =============================================================================

# This programme is private, no copy or other uses are allowed without the authors permision.

import os
import random 
import sys 
import sip
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from IOFilesClass import IOFiles
import pandas as pd 

import numpy as np 
from pyqtgraph import PlotWidget, mkPen, ViewBox, intColor, plot
import pyqtgraph as pg 
import math
from numpy import asarray, zeros, array, argmax, append, linspace, insert, shape, arange, array_equal, multiply, array2string, transpose, savetxt, concatenate


# from Main_MapsiSuite import MainWindow
# from Mapsi_Suite_GUI import Ui_MainWindow
# from tmm1d import TMM
# from scipy.signal import find_peaks, peak_prominences, peak_widths


class AnalysisGUI(QtCore.QObject):
    

    count = 0
    wavelength = np.linspace(2.5, 25, 10000)

    # Initialization
    def __init__(self, gui_pointer):     # When the class is created
    
        super(AnalysisGUI,self).__init__()
        self.gui_pointer = gui_pointer
        # self.rowPosition = self.gui_pointer.tableWidget_analysis.rowCount()
        
        self.AnalysisDataPointer = AnalysisData()
        self.GeneratePlotLayout()
        
        self.gui_pointer.pushButton_AnalysisAddFile.clicked.connect(lambda: self.opennewfilebutton())
        self.gui_pointer.pushButtonClear.clicked.connect(lambda: self.clearfilesbutton())
        self.gui_pointer.pushButtonCombine.clicked.connect(lambda: self.combinebutton())
        self.gui_pointer.doubleSpinBox_Wavelengthmin.valueChanged.connect(lambda: self.changevaluerange())
        self.gui_pointer.doubleSpinBox_wavelengthmax.valueChanged.connect(lambda: self.changevaluerange())
        self.gui_pointer.doubleSpinBox_tramin.valueChanged.connect(lambda: self.changevaluerange())
        self.gui_pointer.doubleSpinBox_tramax.valueChanged.connect(lambda: self.changevaluerange())
        self.gui_pointer.tableWidget_analysis.itemChanged.connect(lambda: self.changevalue())
        # self.gui_pointer.tableWidget_analysis.itemSelectionChanged.connect(lambda: self.viewchange())
        
    
        
    def opennewfilebutton(self):
        row = self.gui_pointer.tableWidget_analysis.currentRow()
        col = self.gui_pointer.tableWidget_analysis.currentColumn()
        newfile= QFileDialog.getOpenFileName()
        a = IOFiles.readFTIRfile(newfile[0])
        x = (a.iloc[:,0])
        y = (a.iloc[:,1])
        x = x[::-1]
        y = y[::-1]
        
        if newfile[0] in self.AnalysisDataPointer.name:
            pass
        else:
            self.AnalysisDataPointer.NewDatax(x)
            self.AnalysisDataPointer.NewDatay(y)
            self.AnalysisDataPointer.Values(1)
            self.AnalysisDataPointer.Name(newfile[0])
            interpolation = np.interp(AnalysisGUI.wavelength, x, y)
            self.AnalysisDataPointer.NewFTIRInterpolatedData(interpolation)
            self.PlotResults()
            rowPosition = self.gui_pointer.tableWidget_analysis.rowCount()
            self.gui_pointer.tableWidget_analysis.insertRow(rowPosition)
            self.gui_pointer.tableWidget_analysis.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(newfile[0][50:-3])))
            self.gui_pointer.tableWidget_analysis.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(1)))
            self.gui_pointer.tableWidget_analysis.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(0)))
            self.gui_pointer.tableWidget_analysis.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(1)))
            self.gui_pointer.tableWidget_analysis.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(0)))
            self.gui_pointer.tableWidget_analysis.setCellWidget(rowPosition, 5, QtWidgets.QCheckBox())
            self.gui_pointer.tableWidget_analysis.setCellWidget(rowPosition, 6, QtWidgets.QCheckBox())
            self.gui_pointer.tableWidget_analysis.cellWidget(rowPosition,5).setChecked(True)
            self.gui_pointer.tableWidget_analysis.cellWidget(rowPosition,6).stateChanged.connect(lambda:self.deletechange())
            self.gui_pointer.tableWidget_analysis.cellWidget(rowPosition,5).stateChanged.connect(lambda:self.viewchange())
            print(rowPosition)
        
  
        
     
        
    def changevalue(self):
        
        
        row = self.gui_pointer.tableWidget_analysis.currentRow()
        col = self.gui_pointer.tableWidget_analysis.currentColumn()
        
        if col == 1 or 2:
            newx = ((self.AnalysisDataPointer.datax[row] * float(self.gui_pointer.tableWidget_analysis.item(row,1).text())) + float(self.gui_pointer.tableWidget_analysis.item(row,2).text())) 
        if col == 3 or 4:
            newy = ((self.AnalysisDataPointer.datay[row] * float(self.gui_pointer.tableWidget_analysis.item(row,3).text())) + float(self.gui_pointer.tableWidget_analysis.item(row,4).text()))  
        
        interpolation = np.interp(AnalysisGUI.wavelength, newx, newy)
        self.AnalysisDataPointer.FTIR_Trans[row] = interpolation 
        self.PlotResults()

        # if self.gui_pointer.tableWidget_analysis.cellWidget(row,5).stateChanged:
        #     if self.gui_pointer.tableWidget_analysis.cellWidget(row,5).isChecked():
        #         self.AnalysisDataPointer.values[row] = 1
        #         self.PlotResults()
        #         print(self.AnalysisDataPointer.values)
            
        #     else: 
        #         self.AnalysisDataPointer.values[row] = 0
        #         self.PlotResults
        #         print(self.AnalysisDataPointer.values)
            
                
        # if self.gui_pointer.tableWidget_analysis.cellWidget(row,6).stateChanged and col == 6:
        #     del(self.AnalysisDataPointer.datax[row])
        #     del self.AnalysisDataPointer.datay[row]
        #     del self.AnalysisDataPointer.FTIR_Trans[row]
        #     del self.AnalysisDataPointer.values[row]
        #     del self.AnalysisDataPointer.name[row]
        #     self.gui_pointer.tableWidget_analysis.removeRow(row)
        #     self.PlotResults()
        
        
    def viewchange(self):
        
        row = self.gui_pointer.tableWidget_analysis.currentRow()
        col = self.gui_pointer.tableWidget_analysis.currentColumn()
        
        if self.gui_pointer.tableWidget_analysis.cellWidget(row,5).isChecked():
            self.AnalysisDataPointer.values[row] = 1
            print(self.AnalysisDataPointer.values)
        
        
        else: 
            self.AnalysisDataPointer.values[row] = 0
            print(self.AnalysisDataPointer.values)
        
        self.PlotResults()
    
        

                
    def deletechange(self):
        row = self.gui_pointer.tableWidget_analysis.currentRow()
        col = self.gui_pointer.tableWidget_analysis.currentColumn()
        
                           
        if self.gui_pointer.tableWidget_analysis.cellWidget(row,6).isChecked():
            del(self.AnalysisDataPointer.datax[row])
            del self.AnalysisDataPointer.datay[row]
            del self.AnalysisDataPointer.FTIR_Trans[row]
            del self.AnalysisDataPointer.values[row]
            del self.AnalysisDataPointer.name[row]
            self.gui_pointer.tableWidget_analysis.removeRow(row)
            self.PlotResults()
        

            
        
        
        
            

    def changevaluerange(self):
        #TODO: Read user input value
        self.p1.setLimits(xMin= self.gui_pointer.doubleSpinBox_Wavelengthmin.value(), xMax= self.gui_pointer.doubleSpinBox_wavelengthmax.value(), yMin= self.gui_pointer.doubleSpinBox_tramin.value(), yMax= self.gui_pointer.doubleSpinBox_tramax.value())
        self.p2.setLimits(xMin= self.gui_pointer.doubleSpinBox_Wavelengthmin.value(), xMax= self.gui_pointer.doubleSpinBox_wavelengthmax.value(), yMin= self.gui_pointer.doubleSpinBox_tramin.value(), yMax= self.gui_pointer.doubleSpinBox_tramax.value())
        self.p1.informViewBoundsChanged()
        self.p2.informViewBoundsChanged()
  
        
    def clearfilesbutton(self):        
        self.gui_pointer.graphicsViewAnalysis1.clear()
        self.gui_pointer.graphicsViewAnalysis2.clear()
        self.AnalysisDataPointer.clearfiles()
        self.gui_pointer.tableWidget_analysis.setRowCount(0)
    
            
    def combinebutton(self):
        self.p2.clear()
        tracombine = []
        
        for i in range(len(self.AnalysisDataPointer.values)):
            if self.AnalysisDataPointer.values[i] == 1:
                tracombine.append(self.AnalysisDataPointer.FTIR_Trans[i])
            else:
                continue
        data = pd.DataFrame(tracombine)
        data = data.prod()
        data = data / (100  ** (len(tracombine) - 1))
        self.AnalysisDataPointer.FTIR_Combine = data
        self.PlotResultsCombination()
        self.AnalysisDataPointer.clearCombineFiles()


    # Generate the plot layout
    def GeneratePlotLayout(self): 
        #  Tra & Wav Graph
        self.gui_pointer.graphicsViewAnalysis1.setBackground('w')#setConfigOption('background', 'w')        
        self.p1=self.gui_pointer.graphicsViewAnalysis1.plotItem
        styles = {'color':'#ff3333', 'font-size':'20px'}
        self.p1.getAxis('left').setLabel('Tra', **styles)
        styles = {'color':'r', 'font-size':'20px'}
        self.gui_pointer.graphicsViewAnalysis1.setLabel('bottom', 'Wavelength (um)',**styles)
        
        
        self.gui_pointer.graphicsViewAnalysis2.setBackground('w')#setConfigOption('background', 'w')        
        self.p2=self.gui_pointer.graphicsViewAnalysis2.plotItem
        styles = {'color':'#ff3333', 'font-size':'20px'}
        self.p2.getAxis('left').setLabel('Tra', **styles)
        styles = {'color':'r', 'font-size':'20px'}
        self.gui_pointer.graphicsViewAnalysis1.setLabel('bottom', 'Wavelength (um)',**styles)

        
        
    def PlotResults(self):
        self.p1.clear()
        a = 0
        for i in range(len(self.AnalysisDataPointer.values)):
            newcolor = [[255,0,0], [0, 255, 0],[0, 0, 255],[225, 0, 225], [255, 255, 0], [0, 255, 255], [0,0,0]]
            pen = pg.mkPen(color = newcolor[a])
            if self.AnalysisDataPointer.values[int(i)] == 1:
                self.p1.plot(AnalysisGUI.wavelength, self.AnalysisDataPointer.FTIR_Trans[int(i)], pen =pen)
            else:
                continue
            a += 1
            
   
    def PlotResultsCombination(self):

        newcolor = list(np.random.choice(range(256), size=3))
        pen = pg.mkPen(color = newcolor)
        self.p2.plot(AnalysisGUI.wavelength,self.AnalysisDataPointer.FTIR_Combine,pen=pen)
        


   
# =============================================================================
# Analysis Class data        
# =============================================================================
class AnalysisData():
    def __init__(self):     # When the class is created
        # Interpolated FTIR_DAta
        self.FTIR_Trans = []
        self.FTIR_Combine = []
        self.datax = []
        self.datay = []
        self.delete = []
        self.values = []
        self.name= []
        
    def Name(self, name)   :
        self.name.append(name)
    
    def NewDatax(self, addition):
        self.datax.append(addition)
        
    def NewDatay(self, addition):
        self.datay.append(addition)
    
    def NewFTIRInterpolatedData(self, In_Transmittance):
        self.FTIR_Trans.append(In_Transmittance)

    def Values(self, value):
        self.values.append(value)        
        
    def clearfiles(self):
        self.FTIR_Trans = []
        self.FTIR_Combine = []
        self.datax = []
        self.datay = []
        self.delete = []
        self.name = []
        self.values = []
        
    def clearCombineFiles(self):
        self.FTIR_Combine = []
        
        

    
    