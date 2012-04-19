import sys 
import os
import shlex

from PyQt4 import QtCore
from PyQt4 import QtGui

class Console(QtGui.QPlainTextEdit):
    def __init__(self, parent=None):
        QtGui.QPlainTextEdit.__init__(self, parent)
        
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.setUndoRedoEnabled(False)
        self.setReadOnly(True)
        self.document().setDefaultFont(QtGui.QFont("monospace", 9, QtGui.QFont.Normal))
        
        self.contents = ""
        self.line_buffer = QtGui.QLineEdit()
        self.process = QtCore.QProcess(self)
        
        self.process.started.connect(self.on_started)
        self.process.readyReadStandardOutput.connect(self.on_stdout)
        self.process.error.connect(self.on_error)
        self.process.finished.connect(self.on_finished)
        
    def on_started(self):
        self.setReadOnly(False)
        
    def on_finished(self):
        self.write("[ program terminated ]\n")
        self.setReadOnly(True)
        
    def on_stdout(self):
        data = self.process.readAll()
        self.write(data)
        
    def on_error(self):
        self.write("An error occurred: %s" % str(self.process.error()))
        
    def clear(self):
        self.contents = ""
        self.line_buffer.setText("")
        self.redraw()
        
    def redraw(self):
        self.setPlainText(self.contents + self.line_buffer.text())
        cursor_offset = len(self.line_buffer.text()) - self.line_buffer.cursorPosition()
        self.moveCursor(QtGui.QTextCursor.End)
        for i in range(cursor_offset):
            self.moveCursor(QtGui.QTextCursor.Left, QtGui.QTextCursor.MoveAnchor)
        
    def write(self, data):
        self.contents += str(data)
        self.redraw()
        
    def commit_buffer(self):
        data = self.line_buffer.text() + "\n"
        self.line_buffer.setText("")
        self.write(data)
        if self.process is not None:
            self.process.writeData(data)
        
    def keyPressEvent(self, event):
        #TODO: This should allow modifiers and other things of this sort so that users can copy and paste stuff out of the console
        if not self.isReadOnly():
            if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
                self.commit_buffer()
            else:
                self.line_buffer.keyPressEvent(event)
                self.redraw()
            
    def run(self, filename, args_string):
        self.clear()
        args = shlex.split(args_string)
        self.process.start(QtCore.QString(filename), QtCore.QStringList(args))

