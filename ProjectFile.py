import os
from PyQt4 import QtCore
from FileEditor import FileEditor
from FloatingNotification import FloatingNotification

class ProjectFile(FileEditor):
    modificationStateChanged = QtCore.pyqtSignal(QtCore.QObject)
    removalConfirmed = QtCore.pyqtSignal(QtCore.QObject)
    
    def __init__(self, filename, file_path):
        FileEditor.__init__(self, None)
        
        self.filename = filename
        self.file_path = file_path
        self.filehandle = QtCore.QFile(self.file_path)
        self.read_file_contents()
        
        self.selectionChanged.connect(self.on_selection_changed)
        self.modificationChanged.connect(self.on_modification_changed)
        
        #Used to keep track of what search the current selection is a result of.
        # None indicates that the current selection is not the result of a search operation.
        self.current_search_selection = None
        
        self.externally_modified_notification = FloatingNotification(self, "resources/ExternallyModified.ui")
        self.externally_modified_notification.hide()
        
        self.externally_modified_notification.buttonbox.accepted.connect(self.on_ext_mod_notify_reload)
        self.externally_modified_notification.buttonbox.rejected.connect(self.on_ext_mod_notify_noreload)
        
        self.externally_removed_notification = FloatingNotification(self, "resources/ExternallyRemoved.ui")
        self.externally_removed_notification.hide()
        
        self.externally_removed_notification.buttonbox.accepted.connect(self.on_ext_rem_notify_keep)
        self.externally_removed_notification.buttonbox.rejected.connect(self.on_ext_rem_notify_nokeep)
        
        self.appear_modified = False
        
        self.last_modified = os.path.getmtime(self.file_path)
        
    def read_file_contents(self):
        if self.filehandle is not None:
        
            self.filehandle.open(QtCore.QIODevice.ReadOnly)
            self.read(self.filehandle)
            self.filehandle.close()
            
            self.setModified(False)
            self.appear_modified = False
            self.last_modified = os.path.getmtime(self.file_path)
        
    def write_file_contents(self):
        if self.filehandle is not None:
        
            self.filehandle.open(QtCore.QIODevice.WriteOnly)
            self.write(self.filehandle)
            self.filehandle.close()
            
            self.setModified(False)
            self.appear_modified = False
            self.last_modified = os.path.getmtime(self.file_path)
            
    def externally_modified(self):
        try:
            return self.last_modified != os.path.getmtime(self.file_path)
        except OSError:
            return True
        
    def on_ext_mod_notify_reload(self):
        self.read_file_contents()
        self.setReadOnly(False)
        self.externally_modified_notification.hide()
        
    def on_ext_mod_notify_noreload(self):
        self.appear_modified = True
        self.on_modification_changed(True)
        self.setReadOnly(False)
        self.externally_modified_notification.hide()
        
    def on_ext_rem_notify_keep(self):
        self.write_file_contents()
        
    def on_ext_rem_notify_nokeep(self):
        self.removalConfirmed.emit(self)
    
    def on_selection_changed(self):
        self.current_search_selection = None
    
    def save(self):
        "Save this file"
        self.write_file_contents()
    
    def close(self):
        self.filehandle.close()
        self.filehandle = None
    
    @property
    def modified(self):
        "Check if the file is modified compared to the saved version."
        return self.isModified() or self.appear_modified

    @property
    def extension(self):
        return self.filename.split(".")[-1]

    def on_modification_changed(self, value):
        self.modificationStateChanged.emit(self)


