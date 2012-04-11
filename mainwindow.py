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
        
        self.new_file_dialog = QtGui.QInputDialog(self)
        self.new_file_dialog.setOkButtonText(QtCore.QString("Create"))
        self.new_file_dialog.setLabelText(QtCore.QString("Enter the filename:"))
        self.new_file_dialog.setModal(True)
        
        self.new_file_dialog.accepted.connect(self.on_new_file_accepted)
        self.new_file_dialog.rejected.connect(self.on_new_file_rejected)

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

    def on_new_file(self):
        self.new_file_dialog.open()
        
    def on_new_file_accepted(self):
    	print "new file accepted"
    	
    def on_new_file_rejected(self):
    	print "new file rejected"
        
    def on_cut(self):
    	current_editor = self.editor_tab_widget.currentWidget()
    	if current_editor is not None:
    		current_editor.cut()
    	
    def on_copy(self):
    	current_editor = self.editor_tab_widget.currentWidget()
    	if current_editor is not None:
    		current_editor.copy()
    	
    def on_paste(self):
    	current_editor = self.editor_tab_widget.currentWidget()
    	if current_editor is not None:
    		current_editor.paste()
    	
    def on_select_all(self):
    	current_editor = self.editor_tab_widget.currentWidget()
    	if current_editor is not None:
    		current_editor.selectAll(True)
    	
    def on_undo(self):
    	current_editor = self.editor_tab_widget.currentWidget()
    	if current_editor is not None:
    		current_editor.undo()
    	
    def on_redo(self):
    	current_editor = self.editor_tab_widget.currentWidget()
    	if current_editor is not None:
    		current_editor.redo()
    		
    def on_reformat(self):
    	print "Someone pressed reformat; The fool."

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
