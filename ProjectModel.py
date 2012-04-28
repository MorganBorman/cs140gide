'''
A class which maintains the set of scintilla editors, filehandles, and filenames
Associated with the current project.

'''
import os, fnmatch, shutil
#from SourceEditor import SourceEditor
from PyQt4 import QtCore
from PyQt4 import Qsci
from PyQt4 import QtGui
# import QsciScintilla, QsciLexerCPP

class FileEditor(Qsci.QsciScintilla):
    """
    The settings and configuration of this class are based on the example tutorial by Eli Bendersky.
    http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt/
    """
    
    def __init__(self, parent):
        Qsci.QsciScintilla.__init__(self)
        
        # Set the default font
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)
        
        # Margin 0 is used for line numbers 
        
        fontmetrics = QtGui.QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("0000"))
        self.setMarginLineNumbers(10, True)
        self.setMarginsBackgroundColor(QtGui.QColor("#cccccc"))
        
        self.setWhitespaceVisibility(self.WsVisible)
        
        self.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
        
        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QtGui.QColor("#ffe4e4"))
        
        lexer = Qsci.QsciLexerCPP()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        self.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)
        #self.SendScintilla(Qsci.QsciScintilla.SCI_SETSCROLLWIDTH, 10)
        #self.SendScintilla(Qsci.QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)
        
        # not too small
        self.setMinimumSize(200, 200)


class ProjectFile(FileEditor):
    modificationStateChanged = QtCore.pyqtSignal(QtCore.QObject)
    
    def __init__(self, parent_model, filename, file_path):
        FileEditor.__init__(self, None)
        
        self.parent_model = parent_model
        self.filename = filename
        self.file_path = file_path
        self.filehandle = QtCore.QFile(self.file_path)
        self.filehandle.open(QtCore.QIODevice.ReadWrite)
        
        self.read(self.filehandle)
        
        self.setModified(False)
        
        self.selectionChanged.connect(self.on_selection_changed)
        self.modificationChanged.connect(self.on_modification_changed)
        
        #Used to keep track of what search the current selection is a result of.
        # None indicates that the current selection is not the result of a search operation.
        self.current_search_selection = None
    
    def on_selection_changed(self):
        self.current_search_selection = None
    
    def save(self):
        "Save this file"
        if self.filehandle != None:
            self.filehandle.seek(0)
            self.filehandle.resize(0)
            self.write(self.filehandle)
            self.filehandle.flush()
            self.setModified(False)
    
    def close(self):
        self.filehandle.close()
        self.filehandle = None
    
    @property
    def modified(self):
        "Check if the file is modified compared to the saved version."
        return self.isModified()
    
    def on_modification_changed(self, value):
        self.modificationStateChanged.emit(self)

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
        
        #Keep track of the current project directory
        self.project_directory = None
        
        #List of the editors associated with this project
        self.file_editors = []
    
    def open(self, project_directory):
        "Tell the project model that we want to open a new/existing project."
        self.close()
        
        if self.closed:
            self.project_directory = project_directory
        
            for filename in os.listdir(str(project_directory)):
                if fnmatch.fnmatch(filename, '*.cpp') or fnmatch.fnmatch(filename, '*.h'):
                    self.__open_file(filename)
                    
            self.projectOpened.emit(True)
        
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
        
        file_editor = ProjectFile(self, filename, full_path)
        file_editor.modificationStateChanged.connect(self.on_file_modification_state_changed)
        
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
            file_editor.save()
    
    def save_all(self):
        "Tell this project model to save all file_editors."
        for file_editor in self.file_editors:
            file_editor.save()
    
    @property
    def closed(self):
        return self.project_directory == None and len(self.file_editors) == 0

