# =============================================================================
# Mapsi Photonics 
# Simulation Class
# Version PyQt5
# Daniel Segura May 2021
# =============================================================================

# This programme is private, no copy or other uses are allowed without the authors permision.

import os
import sip
import IO_Files
from PyQt5 import QtWidgets, QtCore, QtGui


from pyqtgraph import PlotWidget, mkPen, ViewBox

# from Main_MapsiSuite import MainWindow
# from Mapsi_Suite_GUI import Ui_MainWindow
from SourceClass import Source
from DeviceClass import Device
from math import pi
from numpy import ones, real, imag, zeros, loadtxt, absolute, interp, full, array, argmax, append, linspace, insert, delete, shape, arange, array_equal, random
from tmm1d import TMM
from scipy.signal import find_peaks, peak_prominences, peak_widths
import MP_Functions


class OptimizationGUI(QtCore.QObject):

    # Initialization
    def __init__(self, gui_pointer):     # When the class is created
        super(OptimizationGUI,self).__init__()
        self.gui_pointer = gui_pointer
        self.GeneratePlotLayout()
        
        self.OptimizationData_Object = OptimizationData()

        self.gui_pointer.pushButton_NewRowOptimization.clicked.connect(lambda: self.AddParameterTable())

# tableWidget_Optimization


    # Generate the plot layout
    def GeneratePlotLayout(self): 
        # TRA Graph
        self.gui_pointer.graphicsView_Opt_Trans.setBackground('w')#setConfigOption('background', 'w')
        styles = {'color':'r', 'font-size':'20px'}
        self.gui_pointer.graphicsView_Opt_Trans.setLabel('left', 'TRA',**styles)
        self.gui_pointer.graphicsView_Opt_Trans.setLabel('bottom', 'User Parameter',**styles)
        self.gui_pointer.graphicsView_Opt_Trans.addLegend()

        # TRA Graph
        self.gui_pointer.graphicsView_Opt_Wav.setBackground('w')#setConfigOption('background', 'w')
        styles = {'color':'r', 'font-size':'20px'}
        self.gui_pointer.graphicsView_Opt_Wav.setLabel('left', 'Wavelength',**styles)
        self.gui_pointer.graphicsView_Opt_Wav.setLabel('bottom', 'User Parameter',**styles)
        self.gui_pointer.graphicsView_Opt_Wav.addLegend()

        # TRA Graph
        self.gui_pointer.graphicsView_Opt_FWHM.setBackground('w')#setConfigOption('background', 'w')
        styles = {'color':'r', 'font-size':'20px'}
        self.gui_pointer.graphicsView_Opt_FWHM.setLabel('left', 'FWHM',**styles)
        self.gui_pointer.graphicsView_Opt_FWHM.setLabel('bottom', 'User Parameter',**styles)
        self.gui_pointer.graphicsView_Opt_FWHM.addLegend()

        # TRA Graph
        self.gui_pointer.graphicsView_Opt_BGW.setBackground('w')#setConfigOption('background', 'w')
        styles = {'color':'r', 'font-size':'20px'}
        self.gui_pointer.graphicsView_Opt_BGW.setLabel('left', 'BandGap Width',**styles)
        self.gui_pointer.graphicsView_Opt_BGW.setLabel('bottom', 'User Parameter',**styles)
        self.gui_pointer.graphicsView_Opt_BGW.addLegend()    
        
        
    def AddParameterTable(self):
        NumbRows = self.gui_pointer.table_User.rowCount()
        self.gui_pointer.tableWidget_Optimization.insertRow(NumbRows)
        # Insertar checkbox 
        chkBoxItem = QtWidgets.QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)       
        self.gui_pointer.tableWidget_Optimization.setItem(NumbRows,0,chkBoxItem)

    # TODO:
        # Delete checked rows
        # Generar taula de dades i mecanisme per convertir taula 2D de guardar resultats amb les convinacions d'entraa
        # Llençar simulacions
        # Plotejar
       
    
       
    def SetElements(self):
        if self.TYPE == 0:               
            self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
            self.gridLayout_4.setContentsMargins(6, 6, -1, 6)
            self.gridLayout_4.setObjectName("gridLayout_"+str(self.POSITION))
            self.label_20 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
            self.label_20.setSizePolicy(sizePolicy)
            self.label_20.setObjectName("label_20")
            self.gridLayout_4.addWidget(self.label_20, 0, 5, 1, 1, QtCore.Qt.AlignRight)
            self.label_21 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
            self.label_21.setSizePolicy(sizePolicy)
            self.label_21.setObjectName("label_21")
            self.gridLayout_4.addWidget(self.label_21, 3, 0, 1, 1)
            self.label_22 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
            self.label_22.setSizePolicy(sizePolicy)
            self.label_22.setObjectName("label_22")
            self.gridLayout_4.addWidget(self.label_22, 3, 2, 1, 1)
            self.label_23 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
            self.label_23.setSizePolicy(sizePolicy)
            self.label_23.setObjectName("label_23")
            self.gridLayout_4.addWidget(self.label_23, 3, 4, 1, 1)
            self.Edit_n2 = QtWidgets.QLineEdit(self.groupBox)
            self.Edit_n2.setMaximumSize(QtCore.QSize(25, 16777215))
            self.Edit_n2.setObjectName("Edit_n2")
            self.gridLayout_4.addWidget(self.Edit_n2, 3, 3, 1, 1)
            self.label_Filename = QtWidgets.QLabel(self.groupBox)
            self.label_Filename.setObjectName("label_Filename")
            self.label_Filename.setMaximumSize(QtCore.QSize(300, 16777215))
            self.gridLayout_4.addWidget(self.label_Filename, 0, 0, 1, 5)
            self.checkBox_FixPeriod = QtWidgets.QCheckBox(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.checkBox_FixPeriod.sizePolicy().hasHeightForWidth())
            self.checkBox_FixPeriod.setSizePolicy(sizePolicy)
            self.checkBox_FixPeriod.setObjectName("checkBox_FixPeriod")
            self.gridLayout_4.addWidget(self.checkBox_FixPeriod, 1, 0, 1, 1)
            self.Edit_fix_period = QtWidgets.QLineEdit(self.groupBox)
            self.Edit_fix_period.setObjectName("Edit_fix_period")
            self.gridLayout_4.addWidget(self.Edit_fix_period, 1, 1, 1, 4)
            self.spin_periods = QtWidgets.QSpinBox(self.groupBox)
            self.spin_periods.setObjectName("spin_periods")
            self.gridLayout_4.addWidget(self.spin_periods, 1, 6, 1, 1)
            self.Edit_n = QtWidgets.QLineEdit(self.groupBox)
            self.Edit_n.setMaximumSize(QtCore.QSize(25, 16777215))
            self.Edit_n.setObjectName("Edit_n")
            self.gridLayout_4.addWidget(self.Edit_n, 3, 1, 1, 1)
            self.comboBox = QtWidgets.QComboBox(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
            self.comboBox.setSizePolicy(sizePolicy)
            self.comboBox.setMinimumSize(QtCore.QSize(0, 0))
            self.comboBox.setObjectName("comboBox")
            self.comboBox.addItem("")
            self.comboBox.addItem("")
            self.comboBox.addItem("")
            self.gridLayout_4.addWidget(self.comboBox, 0, 6, 1, 1)
            self.label_24 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
            self.label_24.setSizePolicy(sizePolicy)
            self.label_24.setObjectName("label_24")
            self.gridLayout_4.addWidget(self.label_24, 1, 5, 1, 1, QtCore.Qt.AlignRight)
            self.button_deletegroup = QtWidgets.QPushButton(self.groupBox)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button_deletegroup.setIcon(icon)
            self.button_deletegroup.setObjectName("button_deletegroup")
            self.gridLayout_4.addWidget(self.button_deletegroup, 3, 6, 1, 1)
            self.Button_SearchFile = QtWidgets.QPushButton(self.groupBox)
            self.Button_SearchFile.setMaximumSize(QtCore.QSize(60, 16777215))
            self.Button_SearchFile.setText("")
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("Images/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Button_SearchFile.setIcon(icon1)
            self.Button_SearchFile.setObjectName("Button_SearchFile")
            self.gridLayout_4.addWidget(self.Button_SearchFile, 3, 5, 1, 1)
        if self.TYPE == 1:    
            self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
            self.gridLayout_4.setContentsMargins(6, 6, -1, 6)
            self.gridLayout_4.setObjectName("gridLayout_4")
            self.spin_periods = QtWidgets.QSpinBox(self.groupBox)
            self.spin_periods.setObjectName("spin_periods")
            self.gridLayout_4.addWidget(self.spin_periods, 2, 6, 1, 1)
            self.Edit_n2 = QtWidgets.QLineEdit(self.groupBox)
            self.Edit_n2.setMaximumSize(QtCore.QSize(25, 16777215))
            self.Edit_n2.setObjectName("Edit_n2")
            self.gridLayout_4.addWidget(self.Edit_n2, 4, 3, 1, 1)
            self.table_User = QtWidgets.QTableWidget(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.table_User.sizePolicy().hasHeightForWidth())
            self.table_User.setSizePolicy(sizePolicy)
            font = QtGui.QFont()
            font.setPointSize(8)
            self.table_User.setFont(font)
            self.table_User.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.table_User.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.table_User.setTabKeyNavigation(True)
            self.table_User.setWordWrap(False)
            self.table_User.setObjectName("table_User")
            self.table_User.setColumnCount(3)
            self.table_User.setRowCount(1)
            item = QtWidgets.QTableWidgetItem()
            self.table_User.setVerticalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.table_User.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.table_User.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            self.table_User.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(8)
            item.setFont(font)
            self.table_User.setItem(0, 0, item)
            self.table_User.horizontalHeader().setVisible(True)
            self.table_User.horizontalHeader().setCascadingSectionResizes(False)
            self.table_User.horizontalHeader().setDefaultSectionSize(103)
            self.table_User.horizontalHeader().setHighlightSections(True)
            self.table_User.horizontalHeader().setSortIndicatorShown(False)
            self.table_User.horizontalHeader().setStretchLastSection(False)
            self.table_User.verticalHeader().setVisible(False)
            self.table_User.verticalHeader().setDefaultSectionSize(16)
            self.table_User.verticalHeader().setHighlightSections(True)
            self.table_User.verticalHeader().setMinimumSectionSize(16)
            self.table_User.verticalHeader().setStretchLastSection(False)
            self.gridLayout_4.addWidget(self.table_User, 0, 0, 3, 5)
            self.comboBox = QtWidgets.QComboBox(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
            self.comboBox.setSizePolicy(sizePolicy)
            self.comboBox.setMinimumSize(QtCore.QSize(0, 0))
            self.comboBox.setObjectName("comboBox")
            self.comboBox.addItem("")
            self.comboBox.addItem("")
            self.comboBox.addItem("")
            self.gridLayout_4.addWidget(self.comboBox, 0, 6, 1, 1)
            self.label_26 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
            self.label_26.setSizePolicy(sizePolicy)
            self.label_26.setObjectName("label_26")
            self.gridLayout_4.addWidget(self.label_26, 4, 0, 1, 1)
            self.label_25 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
            self.label_25.setSizePolicy(sizePolicy)
            self.label_25.setObjectName("label_25")
            self.gridLayout_4.addWidget(self.label_25, 0, 5, 1, 1, QtCore.Qt.AlignRight)
            self.button_deletegroup = QtWidgets.QPushButton(self.groupBox)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button_deletegroup.setIcon(icon)
            self.button_deletegroup.setObjectName("button_deletegroup")
            self.gridLayout_4.addWidget(self.button_deletegroup, 4, 6, 1, 1)
            self.Edit_n = QtWidgets.QLineEdit(self.groupBox)
            self.Edit_n.setMaximumSize(QtCore.QSize(25, 16777215))
            self.Edit_n.setObjectName("Edit_n")
            self.gridLayout_4.addWidget(self.Edit_n, 4, 1, 1, 1)
            self.label_28 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
            self.label_28.setSizePolicy(sizePolicy)
            self.label_28.setObjectName("label_28")
            self.gridLayout_4.addWidget(self.label_28, 4, 4, 1, 1)
            self.label_29 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
            self.label_29.setSizePolicy(sizePolicy)
            self.label_29.setObjectName("label_29")
            self.gridLayout_4.addWidget(self.label_29, 2, 5, 1, 1, QtCore.Qt.AlignRight)
            self.label_27 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
            self.label_27.setSizePolicy(sizePolicy)
            self.label_27.setObjectName("label_27")
            self.gridLayout_4.addWidget(self.label_27, 4, 2, 1, 1)
            self.spinBox_Layers = QtWidgets.QSpinBox(self.groupBox)
            self.spinBox_Layers.setObjectName("spinBox")
            self.spinBox_Layers.setValue(1)
            self.gridLayout_4.addWidget(self.spinBox_Layers, 1, 6, 1, 1)
            self.label_13 = QtWidgets.QLabel(self.groupBox)
            self.label_13.setObjectName("label_13")
            self.gridLayout_4.addWidget(self.label_13, 1, 5, 1, 1, QtCore.Qt.AlignRight)
            
            self.spinBox_Layers.valueChanged.connect(lambda: self.ChangeTableSize())

        if self.TYPE == 2:
            self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
            self.gridLayout_4.setContentsMargins(6, 6, -1, 6)
            self.gridLayout_4.setObjectName("gridLayout_4")
            self.label_15 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
            self.label_15.setSizePolicy(sizePolicy)
            self.label_15.setObjectName("label_15")
            self.gridLayout_4.addWidget(self.label_15, 0, 3, 1, 1, QtCore.Qt.AlignRight)
            self.label_Filename = QtWidgets.QLabel(self.groupBox)
            self.label_Filename.setObjectName("label_Filename")
            self.label_Filename.setMaximumSize(QtCore.QSize(300, 16777215))
            self.gridLayout_4.addWidget(self.label_Filename, 0, 0, 1, 3)
            self.Edit_fix_period = QtWidgets.QLineEdit(self.groupBox)
            self.Edit_fix_period.setObjectName("Edit_fix_period")
            self.gridLayout_4.addWidget(self.Edit_fix_period, 1, 1, 1, 2)
            self.comboBox = QtWidgets.QComboBox(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
            self.comboBox.setSizePolicy(sizePolicy)
            self.comboBox.setMinimumSize(QtCore.QSize(0, 0))
            self.comboBox.setObjectName("comboBox")
            self.comboBox.addItem("")
            self.comboBox.addItem("")
            self.comboBox.addItem("")
            self.gridLayout_4.addWidget(self.comboBox, 0, 4, 1, 1)
            self.label_17 = QtWidgets.QLabel(self.groupBox)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
            self.label_17.setSizePolicy(sizePolicy)
            self.label_17.setObjectName("label_17")
            self.gridLayout_4.addWidget(self.label_17, 1, 0, 1, 1)
            self.button_deletegroup = QtWidgets.QPushButton(self.groupBox)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button_deletegroup.setIcon(icon)
            self.button_deletegroup.setObjectName("button_deletegroup")
            self.gridLayout_4.addWidget(self.button_deletegroup, 1, 4, 1, 1)
            self.Button_SearchFile = QtWidgets.QPushButton(self.groupBox)
            self.Button_SearchFile.setMaximumSize(QtCore.QSize(60, 16777215))
            self.Button_SearchFile.setText("")
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("Images/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Button_SearchFile.setIcon(icon1)
            self.Button_SearchFile.setObjectName("Button_SearchFile")
            self.gridLayout_4.addWidget(self.Button_SearchFile, 1, 3, 1, 1)          

    def TranslateGroupBox(self):           
            _translate = QtCore.QCoreApplication.translate
            if self.TYPE == 0:
                self.groupBox.setTitle(_translate("MainWindow", "Periodicity Group"))
                self.label_20.setText(_translate("MainWindow", "Method"))
                self.label_21.setText(_translate("MainWindow", "period = p + "))
                self.label_22.setText(_translate("MainWindow", "n +"))
                self.label_23.setText(_translate("MainWindow", "n^2"))
                self.label_Filename.setText(_translate("MainWindow", "File:"))
                self.checkBox_FixPeriod.setText(_translate("MainWindow", "Set period (p)"))
                self.comboBox.setItemText(0, _translate("MainWindow", "Load file"))
                self.comboBox.setItemText(1, _translate("MainWindow", "User defined"))
                self.comboBox.setItemText(2, _translate("MainWindow", "Dispersive"))
                self.label_24.setText(_translate("MainWindow", "Periods"))
                self.button_deletegroup.setText(_translate("MainWindow", "Delete"))
            if self.TYPE == 1:  
                self.groupBox.setTitle(_translate("MainWindow", "Periodicity Group"))
                item = self.table_User.verticalHeaderItem(0)
                item.setText(_translate("MainWindow", "Nueva fila"))
                item = self.table_User.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "Permitivity"))
                item = self.table_User.horizontalHeaderItem(1)
                item.setText(_translate("MainWindow", "Permeability"))
                item = self.table_User.horizontalHeaderItem(2)
                item.setText(_translate("MainWindow", "Length"))
                __sortingEnabled = self.table_User.isSortingEnabled()
                self.table_User.setSortingEnabled(False)
                self.table_User.setSortingEnabled(__sortingEnabled)
                self.comboBox.setItemText(0, _translate("MainWindow", "Load file"))
                self.comboBox.setItemText(1, _translate("MainWindow", "User defined"))
                self.comboBox.setItemText(2, _translate("MainWindow", "Dispersive"))
                self.label_26.setText(_translate("MainWindow", "period = p + "))
                self.label_25.setText(_translate("MainWindow", "Method"))
                self.button_deletegroup.setText(_translate("MainWindow", "Delete "))
                self.label_28.setText(_translate("MainWindow", "n^2"))
                self.label_29.setText(_translate("MainWindow", "Periods"))
                self.label_27.setText(_translate("MainWindow", "n +"))        
                self.label_13.setText(_translate("MainWindow", "Layers"))  
            if self.TYPE == 2:
                self.groupBox.setTitle(_translate("MainWindow", "Periodicity Group"))
                self.label_15.setText(_translate("MainWindow", "Method"))
                self.label_Filename.setText(_translate("MainWindow", "File:"))
                self.comboBox.setItemText(0, _translate("MainWindow", "Load file"))
                self.comboBox.setItemText(1, _translate("MainWindow", "User defined"))
                self.comboBox.setItemText(2, _translate("MainWindow", "Dispersive"))
                self.label_17.setText(_translate("MainWindow", "Layer length"))
                self.button_deletegroup.setText(_translate("MainWindow", "Delete "))                

    def ChangeTableSize(self):
        NumbRows = self.table_User.rowCount()
        if self.spinBox_Layers.value()>NumbRows:
             self.table_User.insertRow(NumbRows)
        elif self.spinBox_Layers.value()<NumbRows+1:
             self.table_User.removeRow(NumbRows-1)     
        # self.swap.emit(*sorted([1, 1]))    


# =============================================================================
# Simulation Class data        
# =============================================================================
class OptimizationData():
    def __init__(self):     # When the class is created
        self.Source = Source() # Create source Class
        self.Device = Device() # Create Device Class
