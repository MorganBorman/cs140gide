#! /usr/bin/env python

from PyQt4 import QtCore, QtGui, uic
from AuxiliaryDialogs import NewFileDialog, OpenProjectDialog, NewProjectDialog, ConfirmDeleteDialog, UnsavedFilesDialog, GotoLineDialog

class MainWindow(QtGui.QMainWindow):
    def __init__(self, project_model):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from .ui file
        uic.loadUi("resources/MainWindow.ui", self)
        
        #A dictionary of the file handles with the filenames as keys
        self.project_model = project_model
        
        #connect slots to the signals which may be emitted by the ProjectModel
        self.project_model.unsavedFiles.connect(self.on_model_unsaved_files)
        self.project_model.fileOpened.connect(self.on_model_file_opened)
        self.project_model.fileClosed.connect(self.on_model_file_closed)
        self.project_model.projectOpened.connect(self.on_model_project_opened_state)
        self.project_model.fileModified.connect(self.on_model_file_modified_state)

        # Names of major widgets we probably need to access
        # self.editor_tab_widget
        # self.program_output
        # self.build_output
        # self.statusbar
        
        #disable these context menus to stop the toolbar being closed
        self.toolbar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.menubar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        
        #add and remove the welcome_widget to make it respond as that object (hack)
        self.editor_tab_widget.clear()
        self.editor_tab_widget.addTab(self.welcome_widget, "Welcome")
        
        for key, value in self.__dict__.items():
            if type(value) == QtGui.QAction:
                self.addAction(value)
        
        #Set actions which require a project to disabled
        self.set_project_actions_enabled(False)
        
        #Instantiate dialogs which we will use.
        self.new_project_dialog = NewProjectDialog(self)
        self.open_project_dialog = OpenProjectDialog(self)
        
        self.new_file_dialog = NewFileDialog(self)
        
        self.confirm_delete_dialog = ConfirmDeleteDialog(self)
        
        self.unsaved_files_dialog = UnsavedFilesDialog(self)
        
        self.goto_line_dialog = GotoLineDialog(self)
        
    def closeEvent(self, event):
        #Trigger the close project event to make sure the project gets closed cleanly
        self.action_close_project.trigger()
        
        #Only exit if the project got closed. 
        if self.project_model.closed:
            event.accept()
        else:
            event.ignore()

    def set_project_actions_enabled(self, value):
        "Enable or disable actions that require a project to be open."
        
        not_toggled_actions = [ 'action_new_project', 'action_open_project', 'action_quit', 'action_about' ]
        
        for actionObject in self.actions():
            if not actionObject.objectName() in not_toggled_actions:
                actionObject.setEnabled(value)
            
    def set_status(self, status_string):
        "Set the current status bar message."
        self.statusbar.showMessage(QtCore.QString(status_string))

    #model signals

    def on_model_unsaved_files(self, unsaved_list):
        "Query the user whether they want to save the list of files before closing the project."
        self.unsaved_files_dialog.set_list(unsaved_list)
        self.unsaved_files_dialog.show()
        
        cancelled = self.unsaved_files_dialog.exec_() == 0
        
        if not cancelled:
            files_to_save = self.unsaved_files_dialog.get_response()
            for filename in files_to_save:
                self.project_model.save(filename)
            
            self.project_model.force_close()

    def on_model_project_opened_state(self, value):
        self.set_project_actions_enabled(value)
        if value:
            index = self.editor_tab_widget.indexOf(self.welcome_widget)
            self.editor_tab_widget.removeTab(index)
            if len(self.editor_tab_widget) == 0:
                self.editor_tab_widget.addTab(self.new_project_widget, "New Project")
        else:
            self.editor_tab_widget.clear()
            self.editor_tab_widget.addTab(self.welcome_widget, "Welcome")
            
    def on_model_file_closed(self, editor):
        index = self.editor_tab_widget.indexOf(editor)
        self.editor_tab_widget.removeTab(index)
        
        if len(self.editor_tab_widget) == 0:
            self.editor_tab_widget.addTab(self.new_project_widget, "New Project")
            
    def on_model_file_modified_state(self, editor, filename, value):
        index = self.editor_tab_widget.indexOf(editor)
        
        if value:
            self.editor_tab_widget.setTabText(index, QtCore.QString("*" + filename))
        else:
            self.editor_tab_widget.setTabText(index, QtCore.QString(filename))

    def on_model_file_opened(self, filename, editor):
        "Add a new tab for the given filename with the editor specified as the widget."
        index = self.editor_tab_widget.indexOf(self.new_project_widget)
        self.editor_tab_widget.removeTab(index)
        
        self.editor_tab_widget.addTab(editor, QtCore.QString(filename))