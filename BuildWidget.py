import sys 
import os
import shlex

from PyQt4 import QtCore
from PyQt4 import QtGui

class ClangCompiler:
    def run(self, process, files, executable):
        args = ["-g", "-Wall"]
        args.extend(files)
        args.extend(["-o", executable])
        process.start(QtCore.QString("clang++"), QtCore.QStringList(args))
    def parse_errors(self, output):
        #TODO: Finish this
        return False #This should be the compiler output

class GnuCompiler:
    def run(self, process, files, executable):
        args = ["-g", "-Wall"]
        args.extend(files)
        args.extend(["-o", executable])
        process.start(QtCore.QString("g++"), QtCore.QStringList(args))

class Build(QtGui.QPlainTextEdit):
    
    #signals emitted by this widget
    compile_success = QtCore.pyqtSignal(list)
    compile_fail = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        QtGui.QPlainTextEdit.__init__(self, parent)

        self.setUndoRedoEnabled(False)
        self.setReadOnly(True)
        self.document().setDefaultFont(QtGui.QFont("monospace", 9, QtGui.QFont.Normal))

        self.compiler = ClangCompiler()
        
        self.contents = ""
        self.process = QtCore.QProcess(self)

        self.process.started.connect(self.on_started)
        self.process.readyReadStandardError.connect(self.on_stderr)
        self.process.error.connect(self.on_error)
        self.process.finished.connect(self.on_finished)

    def on_started(self):
        pass
        
    def on_finished(self):
        if self.process.exitCode() == 0:
            self.write("[ Compilation Successful ]")
        else:
            self.compiler.parse_errors(self.contents)
        
    def on_stderr(self):
        data = self.process.readAllStandardError()
        self.write(data)
        
    def on_error(self):
        self.write("[ The compiler exited with an error: %s ]" % str(self.process.error()))

    def write(self, data):
        self.contents += str(data)
        self.redraw()

    def clear(self):
        self.contents = ""
        self.redraw()

    def redraw(self):
        self.setReadOnly(False)
        self.setPlainText(self.contents)
        self.setReadOnly(True)

    def compile_project(self, files, executable):
        # TODO kill old proccess
        self.clear()
        self.compiler.run(self.process, files, executable)
        
