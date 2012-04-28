#! /usr/bin/env python

from PyQt4 import QtCore, QtGui, uic
from AuxiliaryDialogs import NewFileDialog, OpenProjectDialog, NewProjectDialog, ConfirmDeleteDialog, UnsavedFilesDialog, GotoLineDialog, FindReplaceDialog, AboutDialog
from ConsoleWidget import Console

class MainWindow(QtGui.QMainWindow):
    def __init__(self, project_model):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from .ui file
        uic.loadUi("resources/MainWindow.ui", self)
        
        self.project_model = project_model
        
        #connect slots to the signals which may be emitted by the ProjectModel
        self.project_model.unsavedFiles.connect(self.on_model_unsaved_files)
        self.project_model.fileOpened.connect(self.on_model_file_opened)
        self.project_model.fileClosed.connect(self.on_model_file_closed)
        self.project_model.projectOpened.connect(self.on_model_project_opened_state)
        self.project_model.fileModifiedStateChanged.connect(self.on_model_file_modified_state_change)

        # Names of major widgets we probably need to access
        # self.editor_tab_widget
        # self.program_output
        # self.build_output
        # self.statusbar
        
        self.program_output = Console()
        self.verticalLayout.addWidget(self.program_output)
        
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
        
        self.find_replace_dialog = FindReplaceDialog(self)
        
        self.about_dialog = AboutDialog(self)
        
    def closeEvent(self, event):
    	"Intercept the close event and check that there isn't anything we need to do first."
    	
        #Trigger the close project event to make sure the project gets closed cleanly
        self.action_close_project.trigger()
        
        #Only exit if the project got closed. 
        if self.project_model.closed:
            event.accept()
        else:
            event.ignore()

    def set_project_actions_enabled(self, value):
        "Enable or disable actions that require a project to be open."
        
        not_toggled_actions = [ 'action_new_project', 'action_open_project', 'action_quit', 'action_about', 'action_run' ]
        
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
        
        #synchronously show the unsaved files dialog window
        cancelled = self.unsaved_files_dialog.exec_() == 0
        
        if not cancelled:
            files_to_save = self.unsaved_files_dialog.get_response()
            for filename in files_to_save:
                self.project_model.save(filename)
            
            self.project_model.force_close()

    def on_model_project_opened_state(self, value):
    	"""The current state of whether a project is opened has changed.
    	
    	Enable or disable the project dependent actions.
    	
    	If opening a project with no files then show the new project help info.
    	If closing a project show the welcome info.
    	"""
        self.set_project_actions_enabled(value)
        if value:
            
            #Remove the welcome widget it it is present.
            index = self.editor_tab_widget.indexOf(self.welcome_widget)
            if index >= 0:
                self.editor_tab_widget.removeTab(index)
                
            #Once we've opened the project if there are no files, show the new project help
            if len(self.editor_tab_widget) == 0:
                self.editor_tab_widget.addTab(self.new_project_widget, "New Project")
        else:
            #If closing a project, clear the tabs and display the welcome tab
            self.editor_tab_widget.clear()
            self.editor_tab_widget.addTab(self.welcome_widget, "Welcome")
            
    def on_model_file_closed(self, file_editor):
    	"A model file has closed so close the file_editor tab associated with it."
        index = self.editor_tab_widget.indexOf(file_editor)
        
        if index >= 0:
            self.editor_tab_widget.removeTab(index)
            
            if len(self.editor_tab_widget) == 0:
                self.editor_tab_widget.addTab(self.new_project_widget, "New Project")
            
    def on_model_file_modified_state_change(self, file_editor):
    	"Set whether or not a file tab indicates that the specified file is modified or not."
        
        #If the modified widget is found set it's name +- a * to indicate whether it is modified. 
        index = self.editor_tab_widget.indexOf(file_editor)
        if index >= 0:
            if file_editor.modified:
                self.editor_tab_widget.setTabText(index, QtCore.QString("*" + file_editor.filename))
            else:
                self.editor_tab_widget.setTabText(index, QtCore.QString(file_editor.filename))

    def on_model_file_opened(self, file_editor):
        "Add a new tab for the given filename with the file_editor specified as the widget."
        
        #Remove the new_project widget if it's still displayed
        index = self.editor_tab_widget.indexOf(self.new_project_widget)
        if index >= 0:
            self.editor_tab_widget.removeTab(index)
        
        self.editor_tab_widget.addTab(file_editor, QtCore.QString(file_editor.filename))

