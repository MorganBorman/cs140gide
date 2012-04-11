import os, sys, fnmatch
from PyQt4 import QtGui

#import the resources
from resources import cs140adagide_qrc

#import the components of our application
from ProjectModel import ProjectModel
from MainWindow import MainWindow
from Controller import Controller

#put them together here
app = QtGui.QApplication(sys.argv)

project_model = ProjectModel()
window_view = MainWindow(project_model)
controller = Controller(project_model, window_view)

window_view.show()

sys.exit(app.exec_())