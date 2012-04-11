'''
A class which maintains the set of scintilla editors, filehandles, and filenames
Associated with the current project.

'''

from SourceEditor import SourceEditor
from PyQt4 import QtCore

class ProjectFile(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.filehandle = open(self.file_path, 'rw')
        self.editor = None
        
    def save(self):
        "Save this file"
        pass
    
    @property
    def modified(self):
        "Check if the file is modified compared to the saved version."
        pass

class ProjectModel(QtCore.QObject):
    
    #signals emitted by this model
    unsavedFiles = QtCore.pyqtSignal(list)
    fileOpened = QtCore.pyqtSignal(str, QtCore.QObject)
    fileModified = QtCore.pyqtSignal(str, bool)
    filesClosed = QtCore.pyqtSignal(list)
    statusMessage = QtCore.pyqtSignal(str)
    
    def __init__(self):
        "A model holding the current project."
        QtCore.QObject.__init__(self)
        
        #Keep the current project path
        self.project_path = None
        
        #Dictionary of ProjectFile objects keyed by filename
        self.files = {}
    
    def open(self, project_path):
        "Tell the project model that we want to open a new/existing project."
        self.close_all()
        self.set_project_actions_enabled(True)
        
        self.current_project_path = project_folder
    
        for filename in os.listdir(str(project_folder)):
            if fnmatch.fnmatch(filename, '*.cpp') or fnmatch.fnmatch(filename, '*.h'):
                self.open_file(project_folder, filename)
        
    def close(self):
        "Tell the project model that we want it to close."
        pass
        
    def new(self, filename):
        "Tell the project model that we want a new file by a given name."
        pass
        
    def save(self, filename):
        "Tell this project model to save the file that has the given name."
        pass
    
    def save_all(self, filename):
        "Tell this project model to save all files."
        pass
    
    @property
    def closed(self):
        return self.project_path == None and len(self.files) == 0
        
        
"""
        filename = self.new_file_dialog.textValue()
        print "new file:", filename
        full_path = os.path.join(self.current_project_path, filename)
        
        if os.path.exists(full_path):
            self.view_window.set_status("The specified file '%s' already exists in this project." % filename)
            return
        
    def on_new_file_rejected(self):
        #print "new file cancelled."
        #can't see that we should actually do anything with this one.
        pass
    
    def open_file(self, project_folder, filename):
        "Open the file in the project folder with the given filename."
        source_editor = SourceEditor()
        
        filehandle = open(os.path.join(project_folder, filename), 'rw')

        source_editor.setText(filehandle.read())

        tabname = os.path.basename(filename)

        self.editor_tab_widget.addTab(source_editor, QtCore.QString(tabname))
"""