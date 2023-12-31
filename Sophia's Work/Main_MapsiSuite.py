# =============================================================================
# Mapsi Photonics 
# Main Class
# Version PyQt5
# Daniel Segura May 2021
# =============================================================================

# This programme is private, no copy or other uses are allowed without the authors permision.

import sys
from PyQt5 import QtWidgets
from Mapsi_Suite_GUI_Sophia import Ui_MainWindow
from AnalysisClass import AnalysisGUI


#Main Class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.MapsiGUI = Ui_MainWindow()
        self.MapsiGUI.setupUi(self)
      
        # Create the needed classes
        AnalysisObject = AnalysisGUI(self.MapsiGUI)


# Avoid duplicated executions
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MapsiSuite_app = MainWindow()
    MapsiSuite_app.show()
    MapsiSuite_app.showMaximized()
    sys.exit(app.exec_())