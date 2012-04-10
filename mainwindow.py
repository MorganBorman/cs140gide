#! /usr/bin/env python

import os, sys, fnmatch
from PyQt4 import QtCore, QtGui, uic, QtCore
from SourceEditor import SourceEditor
import cs140adagide_qrc

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from .ui file
        self.ui = uic.loadUi("mainwindow.ui", self)

        # Names of major widgets you probably need to access
        # self.editor_tab_widget
        # self.program_output
        # self.build_output
        # self.statusbar

        self.editors = []

        #with open("test/main.cpp") as source:
        #    self.example_editor.setText(source.read())

        #self.example_editor.fillIndicatorRange(6, 7, 6, 10, 0)
        #self.example_editor.fillIndicatorRange(7, 2, 7, 9, 0)

    def on_build(self):
        print "some hoodlum clicked on build!"

    def on_open_project(self):
        project_folder = QtGui.QFileDialog.getExistingDirectory(self, 'Open file', './')

        for filename in os.listdir(str(project_folder)):
            if fnmatch.fnmatch(filename, '*.cpp') or fnmatch.fnmatch(filename, '*.h'):
                self.open_file(project_folder, filename)

    def open_file(self, project_folder, filename):
        example_editor = SourceEditor()

        with open(project_folder + '/' + filename, 'r') as source:
            example_editor.setText(source.read())

        tabname = os.path.basename(filename)

        self.editor_tab_widget.addTab(example_editor, QtCore.QString(tabname))

        self.editors.append(example_editor)

    def on_new_file(self):
        print "another one clicked on new file."

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
