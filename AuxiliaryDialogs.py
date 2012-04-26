from PyQt4 import QtCore, QtGui, uic

class NewFileDialog(QtGui.QInputDialog):
    def __init__(self, parent):
        QtGui.QInputDialog.__init__(self, parent)
        
        self.setInputMode(QtGui.QInputDialog.TextInput)
        self.setOkButtonText(QtCore.QString("Create"))
        self.setLabelText(QtCore.QString("Enter the filename:"))
        self.setModal(True)
        
class GotoLineDialog(QtGui.QInputDialog):
    def __init__(self, parent):
        QtGui.QInputDialog.__init__(self, parent)
        
        self.setInputMode(QtGui.QInputDialog.IntInput)
        self.setOkButtonText(QtCore.QString("Goto"))
        self.setLabelText(QtCore.QString("Enter the line number:"))
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
        
class ConfirmDeleteDialog(QtGui.QMessageBox):
    def __init__(self, parent):
        QtGui.QMessageBox.__init__(self, parent)
        self.setText("Delete file?");
        self.setInformativeText("Are you sure you want to delete this file?");
        self.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel);
        self.setDefaultButton(QtGui.QMessageBox.Cancel);
        
    def execute(self):
        val = self.exec_()
        if val == QtGui.QMessageBox.Yes:
            return True
        else:
            return False
        
class UnsavedFilesDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        # Set up the user interface from .ui file
        uic.loadUi("resources/UnsavedFilesDialog.ui", self)
        
        self.unsaved_file_table.itemChanged.connect(self.on_table_item_changed)
        
    def get_response(self):
        "Get which of the files the user chose to save."
        file_list = []
        
        if self.unsaved_file_table.rowCount() == 0:
            return []
        
        for row_index in range(self.unsaved_file_table.rowCount()):
            
            row_widget_item = self.unsaved_file_table.item(row_index, 0)
            
            if (row_widget_item is not None) and (row_widget_item.checkState() > 0):
                if row_index < len(self.file_list):
                    file_list.append(self.file_list[row_index])
            
        return file_list
    
    def set_list(self, file_list):
        "Set the list of files to ask the user about."
        self.file_list = file_list
        
        self.unsaved_file_table.setRowCount(len(file_list))
        for row_index in range(len(file_list)):
            item = QtGui.QTableWidgetItem(QtCore.QString(file_list[row_index].filename))
            item.setCheckState(True)
            self.unsaved_file_table.setItem(row_index, 0, item)
            
    def on_table_item_changed(self, item):
        "Set the button text to be clearer about what will happen if they click it with the current selection."
        response_list_len = len(self.get_response())
        
        if response_list_len == len(self.file_list):
            self.save_and_close.setText("Save All and Close")
        elif response_list_len > 0:
            self.save_and_close.setText("Save Selected and Close")
        else:
            self.save_and_close.setText("Discarding All and Close")
    
class AboutDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        # Set up the user interface from .ui file
        uic.loadUi("resources/AboutDialog.ui", self)
        
        self.accepted.connect(self.hide)
