
from PyQt4 import QtCore, QtGui
import sys, os

class Controller(QtCore.QObject):
    def __init__(self, project_model, view_window):
        QtCore.QObject.__init__(self)
        
        self.view_window = view_window
        self.project_model = project_model
        
        missing_slots = False
        
        #connect all the actions to slots here
        for actionObject in self.view_window.actions():
            try:
                slot_name = "on_" + str(actionObject.objectName())
                slot = self.__getattribute__(slot_name)
                actionObject.triggered.connect(slot)
            except AttributeError:
                print "A slot called '%s' should have been a member function of Controller but it was not found." % slot_name
                missing_slots = True
            
        if missing_slots:
            print "Missing Controller slots encountered. Exiting..."
            sys.exit(1)
            
        self.view_window.new_file_dialog.accepted.connect(self.on_new_file_accepted)
        self.view_window.new_project_dialog.fileSelected.connect(self.on_new_project_accepted)
        self.view_window.open_project_dialog.fileSelected.connect(self.on_open_project_accepted)
        
        self.view_window.find_replace_dialog.replace_all.connect(self.on_replace_all)
        self.view_window.find_replace_dialog.replace.connect(self.on_replace)
        self.view_window.find_replace_dialog.find.connect(self.on_find)
        
        self.view_window.goto_line_dialog.accepted.connect(self.on_goto_line_accepted)
        
    #######################################################
    ###            triggered action handlers            ###
    #######################################################
        
    #new project dialog
    
    def on_new_project_accepted(self, filename):
        self.project_model.new_project(str(filename))
        
    #open project dialog
   
    def on_open_project_accepted(self, filename):
        self.project_model.open(str(filename))
   
    #new file dialog
   
    def on_new_file_accepted(self):
        filename = self.view_window.new_file_dialog.textValue()
        self.project_model.new(str(filename))
        
    def on_goto_line_accepted(self):
        line = self.view_window.goto_line_dialog.intValue() - 1
        
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            
            if line > current_editor_widget.lines():
                return
            
            current_editor_widget.setCursorPosition(line, 0)
   
    #file menu
        
    def on_action_new_project(self):
        self.view_window.new_project_dialog.open()

    def on_action_open_project(self):
        self.view_window.open_project_dialog.open()
   
    def on_action_new_file(self):
        self.view_window.new_file_dialog.open()
        
    def on_action_delete_file(self):
        value = self.view_window.confirm_delete_dialog.execute()
        if value:
            current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
            if current_editor_widget is not None:
                self.project_model.delete(current_editor_widget)
    
    def on_action_save(self):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            self.project_model.save(current_editor_widget)
        
    def on_action_save_all(self):
        self.project_model.save_all()
        
    def on_action_close_project(self):
        self.project_model.close()
        
    def on_action_quit(self):
        #print "quit triggered."
        #this is like the only triggered action that the Controller doesn't need to know about directly
        pass
        
    #edit menu
        
    def on_action_undo(self):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            current_editor_widget.undo()
        
    def on_action_redo(self):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            current_editor_widget.redo()
        
    def on_action_cut(self):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            current_editor_widget.cut()
        
    def on_action_copy(self):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            current_editor_widget.copy()
        
    def on_action_paste(self):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            current_editor_widget.paste()
        
    def on_action_select_all(self):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            current_editor_widget.selectAll()
        
    def on_action_find_replace(self):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            self.view_window.find_replace_dialog.open()
            
    def on_replace_all(self, check_states, search_for, replace_with):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            
            search_description_tuple = (search_for, check_states['match case'], check_states['match entire word'], check_states['wrap around'], check_states['search backward'])
            
            if current_editor_widget.current_search_selection != search_description_tuple:
                self.on_find(check_states, search_for)
                
            while current_editor_widget.current_search_selection == search_description_tuple:
                current_editor_widget.replace(replace_with)
                
                selection_start_row, selection_start_col, selection_end_row, selection_end_col = current_editor_widget.getSelection()
                
                current_editor_widget.setCursorPosition(selection_end_row, selection_end_col)
                
                self.on_find(check_states, search_for)
    
    def on_replace(self, check_states, search_for, replace_with):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            
            search_description_tuple = (search_for, check_states['match case'], check_states['match entire word'], check_states['wrap around'], check_states['search backward'])
            
            if current_editor_widget.current_search_selection != search_description_tuple:
                self.on_find(check_states, search_for)
                
            if current_editor_widget.current_search_selection == search_description_tuple:
                current_editor_widget.replace(replace_with)
                
                selection_start_row, selection_start_col, selection_end_row, selection_end_col = current_editor_widget.getSelection()
                
                current_editor_widget.setCursorPosition(selection_end_row, selection_end_col)
                
                self.on_find(check_states, search_for)
    
    def on_find(self, check_states, search_for):
        current_editor_widget = self.view_window.editor_tab_widget.currentWidget()
        if current_editor_widget is not None:
            
            search_description_tuple = (search_for, check_states['match case'], check_states['match entire word'], check_states['wrap around'], check_states['search backward'])
            
            if current_editor_widget.current_search_selection == search_description_tuple:
                was_found = current_editor_widget.findNext()
            else:
                was_found = current_editor_widget.findFirst(    search_for,
                                                                False,
                                                                check_states['match case'],
                                                                check_states['match entire word'],
                                                                check_states['wrap around'],
                                                                not check_states['search backward']
                                                            )
                """
                Coppied from the c++ documentation.
                
                wasFound = QScintillaEditor.findFirst(
                                                        QString   expr,
                                                        bool      re,
                                                        bool      cs,
                                                        bool      wo,
                                                        bool      wrap,
                                                        bool      forward = true,
                                                        int      line = -1,
                                                        int      index = -1,
                                                        bool      show = true,
                                                        bool      posix = false
                                                    )
                """
            
            if was_found:
                #Set a variable indicating the the current selection is the result of a search.
                current_editor_widget.current_search_selection = search_description_tuple
                
    def on_action_goto_line(self):
        if current_editor_widget is not None:
            self.view_window.goto_line_dialog.setIntRange(0, current_editor_widget.lines())
        
            self.view_window.goto_line_dialog.open()
            
    def on_action_reformat(self):
        print "reformat triggered."
        
    #action menu
        
    def on_action_build(self):
        executable = os.path.join(self.project_model.project_directory, "a.out")
        files = self.project_model.filenames
        self.view_window.build_output.compile_project(files, executable)
        print "Controller: Build triggered. Files " + str(files)
        
    def on_action_run(self):
        #TODO: the name of the exec should come from the project.
        executable = os.path.join(self.project_model.project_directory, "a.out") 
        arguments = str(self.view_window.program_arguments.text())
        self.view_window.program_output.run_program(executable, arguments)
        print "Controller: Run triggered. Arguments line '%s'" % arguments
        
    #help menu
    
    def on_action_about(self):
        self.view_window.about_dialog.open()
        
