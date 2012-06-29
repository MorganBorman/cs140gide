'''
A class which maintains the set of scintilla editors, filehandles, and filenames
Associated with the current project.

'''
import os, fnmatch, shutil
import os.path
from PyQt4 import QtCore
from PyQt4 import QtGui
from ProjectFile import ProjectFile

class ProjectModel(QtCore.QObject):
    
    #signals emitted by this model
    projectOpened = QtCore.pyqtSignal(bool)
    unsavedFiles = QtCore.pyqtSignal(list)
    fileOpened = QtCore.pyqtSignal(QtCore.QObject)
    fileClosed = QtCore.pyqtSignal(QtCore.QObject)
    fileModifiedStateChanged = QtCore.pyqtSignal(QtCore.QObject)
    statusMessage = QtCore.pyqtSignal(str)
    
    def __init__(self):
        "A model holding the current project."
        QtCore.QObject.__init__(self)
        
        # Keep track of the current project directory
        self.project_directory = None
        
        # List of the editors associated with this project
        self.file_editors = []
        
        # Keep track of which file is currently being saved
        self.saving_files = []
        
        # Used to watch the files for changes
        self.file_watcher = QtCore.QFileSystemWatcher()
        self.file_watcher.directoryChanged.connect(self.on_project_directory_changed)
    
    def open(self, project_directory):
        "Tell the project model that we want to open a new/existing project."
        self.close()
        
        if self.closed:
            self.project_directory = project_directory
        
            self.refresh_open_files()
                    
            self.projectOpened.emit(True)
            
            self.file_watcher.addPath(project_directory)
            
    def refresh_open_files(self):
        "Opens any unopened source files in the current project."
        
        already_open_filenames = self.filenames
        
        for filename in os.listdir(str(self.project_directory)):
            if fnmatch.fnmatch(filename, '*.cpp') or fnmatch.fnmatch(filename, '*.h'):
                if not os.path.join(self.project_directory, filename) in already_open_filenames:
                    self.__open_file(filename)
        
    def new_project(self, project_directory):
        if os.path.exists(project_directory):
            self.statusMessage.emit("The selected project name already exists. Either choose a different one, or use open to open the existing project.")
            return
        else:
            os.makedirs(project_directory)
        
        if not os.path.exists(project_directory):
            self.statusMessage.emit("There was an error creating the project. Check permissions.")
            return
        
        self.open(project_directory)
        
        if self.project_directory != project_directory:
            shutil.rmtree(project_directory)
                
    def __open_file(self, filename):
        "Helper function to open a file_editor for the current project."
        full_path = os.path.join(self.project_directory, filename)
        
        file_editor = ProjectFile(filename, full_path)
        file_editor.modificationStateChanged.connect(self.on_file_modification_state_changed)
        file_editor.removalConfirmed.connect(self.on_file_removal_confirmed)
        
        self.fileOpened.emit(file_editor)
        self.file_editors.append(file_editor)
        
    def __close_file(self, file_editor):
        "Helper function to close a file_editor for the current project."
        if file_editor not in self.file_editors:
            return
        
        self.file_editors.remove(file_editor)
        file_editor.close()
        
        self.fileClosed.emit(file_editor)
        file_editor.modificationStateChanged.disconnect(self.on_file_modification_state_changed)
        
    def on_file_modification_state_changed(self, file_editor):
        "Just re-emit the signal so that the view can handle it."
        self.fileModifiedStateChanged.emit(file_editor)
        
    def on_file_removal_confirmed(self, file_editor):
        self.__close_file(file_editor)
        
    def on_project_directory_changed(self, directory):
        directory = str(directory)
        
        if not os.path.isdir(self.project_directory):
            self.force_close()
        else:
            for file_editor in self.file_editors:
                if not file_editor.externally_modified():
                    continue
                
                file_editor.setReadOnly(True)
                    
                if os.path.isfile(file_editor.file_path):
                    file_editor.externally_modified_notification.show()
                else:
                    file_editor.externally_removed_notification.show()
                    
            self.refresh_open_files()
        
    def close(self):
        "Tell the project model that we want it to close."
        unsaved = []
        
        for file_editor in self.file_editors:
            if file_editor.modified:
                unsaved.append(file_editor)
        
        if len(unsaved) > 0:
            self.unsavedFiles.emit(unsaved)
        else:
            self.force_close()
                
    def force_close(self):
        "Tell the model to close all file_editors even unsaved ones without issuing unsavedFiles signal."
        
        for file_editor in self.file_editors[:]:
            self.__close_file(file_editor)
            
        if self.project_directory is not None:
            self.file_watcher.removePath(self.project_directory)
            
            self.project_directory = None
            self.projectOpened.emit(False)
        
    def new(self, filename):
        "Tell the project model that we want a new file by a given name."
        if not ( fnmatch.fnmatch(filename, '*.cpp') or fnmatch.fnmatch(filename, '*.h') ):
            self.statusMessage.emit("You must create file_editors with a '.cpp' or '.h' extension.")
            return
        
        full_path = os.path.join(self.project_directory, filename)
        if os.path.exists(full_path):
            self.statusMessage.emit("The specified file '%s' is already in this project directory." % filename)
            return
        
        #create the file
        
        with open(full_path, 'w') as filehandle:
            filehandle.write('')
            
        self.__open_file(filename)
        
    def delete(self, file_editor):
        "Move a file_editor that the user asks to have deleted into the '.project_trash' folder in the project."
        if not file_editor in self.file_editors:
            return
        
        trashes_directory = os.path.join(self.project_directory, ".project_trash")
        if not os.path.exists(trashes_directory):
            os.makedirs(trashes_directory)
            
        self.__close_file(file_editor)
            
        shutil.move(file_editor.file_path, os.path.join(trashes_directory, file_editor.filename))
        
    def save(self, file_editor):
        "Tell this project model to save the file that has the given name."
        
        #Questionable whether we should actually check this
        if file_editor in self.file_editors:
            self.saving_files.append(file_editor.file_path)
            file_editor.save()
    
    def save_all(self):
        "Tell this project model to save all file_editors."
        for file_editor in self.file_editors:
            self.saving_files.append(file_editor.file_path)
            file_editor.save()
    
    @property
    def closed(self):
        return self.project_directory == None and len(self.file_editors) == 0

    @property
    def filenames(self):
        return [os.path.join(self.project_directory, f.filename) for f in self.file_editors]
        
    @property
    def cpp_filenames(self):
        return [os.path.join(self.project_directory, f.filename) for f in self.file_editors if f.extension == "cpp"]

