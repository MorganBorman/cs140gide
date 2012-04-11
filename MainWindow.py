#! /usr/bin/env python

import os, sys, fnmatch
from PyQt4 import QtCore, QtGui, uic
import time

class NewFileDialog(QtGui.QInputDialog):
    def __init__(self, parent):
        QtGui.QInputDialog.__init__(self, parent)
        
        self.setOkButtonText(QtCore.QString("Create"))
        self.setLabelText(QtCore.QString("Enter the filename:"))
        self.setModal(True)
        
class OpenProjectDialog(QtGui.QFileDialog):
    def __init__(self, parent):
        QtGui.QFileDialog.__init__(self, parent, QtCore.QString("Open Project Directory"), "./")
        
        self.setFileMode(QtGui.QFileDialog.Directory)
        self.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
        self.setOption(QtGui.QFileDialog.DontUseNativeDialog, True)
        self.setModal(True)
        
class NewProjectDialog(QtGui.QFileDialog):
    def __init__(self, parent):
        QtGui.QFileDialog.__init__(self, parent, QtCore.QString("Create Project Directory"), "./")
        
        self.setFileMode(QtGui.QFileDialog.AnyFile)
        self.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        self.setOption(QtGui.QFileDialog.DontUseNativeDialog, True)
        self.setModal(True)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, project_model):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from .ui file
        uic.loadUi("resources/MainWindow.ui", self)
        
        #A dictionary of the file handles with the filenames as keys
        self.project_model = project_model

        # Names of major widgets you probably need to access
        # self.editor_tab_widget
        # self.program_output
        # self.build_output
        # self.statusbar
        
        self.actions_dict = {}
        
        for key, value in self.__dict__.items():
            if type(value) == QtGui.QAction:
                self.actions_dict[key] = value
        
        #Set actions which require a project to disabled
        self.set_project_actions_enabled(False)
        
        self.new_project_dialog = NewProjectDialog(self)
        self.open_project_dialog = OpenProjectDialog(self)
        
        self.new_file_dialog = NewFileDialog(self)
        
    def closeEvent(self, event):
        print "got close event."
        self.action_close_project.trigger()
        if self.project_model.closed:
            event.accept()
        else:
            event.ignore()

    def set_project_actions_enabled(self, value):
        "Set all the actions that depend on having a project enabled/disabled."
        
        toggled_actions = self.actions_dict.keys()
        toggled_actions.remove('action_new_project')
        toggled_actions.remove('action_open_project')
        toggled_actions.remove('action_quit')
        toggled_actions.remove('action_about')
        
        for action in toggled_actions:
            actionObject = self.__dict__[action]
            actionObject.setEnabled(value)
            
    def set_status(self, status_string):
        "Set the current status bar message."
        self.statusbar.showMessage(QtCore.QString(status_string))