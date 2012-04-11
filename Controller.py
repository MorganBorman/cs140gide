
from PyQt4 import QtCore, QtGui
import sys

class Controller(QtCore.QObject):
    def __init__(self, project_model, view_window):
        QtCore.QObject.__init__(self)
        
        self.view_window = view_window
        self.project_model = project_model
        
        #connect all the actions to slots here
        try:
            for actionName, actionObject in self.view_window.actions_dict.items():
                slot_name = "on_" + actionName
                slot = self.__getattribute__(slot_name)
                actionObject.triggered.connect(slot)
        except AttributeError:
            print "A slot called '%s' should have been a member function of Controller but it was not found. Exiting..." % slot_name
            sys.exit(1)
            
        self.view_window.new_file_dialog.accepted.connect(self.on_new_file_accepted)
        self.view_window.new_project_dialog.fileSelected.connect(self.on_new_project_accepted)
        self.view_window.open_project_dialog.fileSelected.connect(self.on_open_project_accepted)
        
    #######################################################
    ###            triggered action handlers            ###
    #######################################################
   
    #new file dialog
   
    def on_new_file_accepted(self):
        filename = self.view_window.new_file_dialog.textValue()
        print "New file accepted:", filename
        
    #open project dialog
    
    def on_new_project_accepted(self, filename):
        print "new project accepted:", filename
   
    def on_open_project_accepted(self, filename):
        print "open project accepted:", filename
   
    #file menu
        
    def on_action_new_project(self):
        self.view_window.new_project_dialog.open()

    def on_action_open_project(self):
        self.view_window.open_project_dialog.open()
   
    def on_action_new_file(self):
        self.view_window.new_file_dialog.open()
    
    def on_action_save(self):
        print "save triggered."
        
    def on_action_save_all(self):
        print "save all triggered."
        
    def on_action_close_project(self):
        self.project_model.close()
        
    def on_action_quit(self):
        print "quit triggered."
        
    #edit menu
        
    def on_action_undo(self):
        print "undo triggered."
        
    def on_action_redo(self):
        print "redo triggered."
        
    def on_action_cut(self):
        print "cut triggered."
        
    def on_action_copy(self):
        print "copy triggered."
        
    def on_action_paste(self):
        print "paste triggered."
        
    def on_action_select_all(self):
        print "select all triggered."
        
    def on_action_find_replace(self):
        print "find replace triggered."
        
    def on_action_goto_line(self):
        print "goto line triggered."
            
    def on_action_reformat(self):
        print "reformat triggered."
        
    #action menu
        
    def on_action_build(self):
        print "build triggered."
        
    def on_action_run(self):
        print "run triggered."
        
    #help menu
    
    def on_action_about(self):
        print "about triggered."
        