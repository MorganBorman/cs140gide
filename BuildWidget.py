import sys 
import os
import shlex
import re

from PyQt4 import QtCore
from PyQt4 import QtGui

class ClangCompiler:
    def run(self, process, files, executable):
        args = ["-g", "-Wall"]
        args.extend(files)
        args.extend(["-o", executable])
        process.start(QtCore.QString("clang++"), QtCore.QStringList(args))
    
    @staticmethod
    def is_id_line(line):
        '''Takes a line and checks to see if it is a clang error message'''
        if len(re.findall(".*:[0-9]+:[0-9]+: (error|warning):.*", line)) == 1:
            return True
        return False

    @staticmethod
    def parse_id_line(line):
        '''Parses a clang line and returns a dict containing the appropriate info'''
        #Todo: this will fail if the filename contains ":"
        elements = line.split(":",4)
        retval = {}
        retval['filename'] = elements[0]
        retval['line_no'] = elements[1]
        retval['char_no'] = elements[2]
        retval['error_type'] = elements[3].strip()
        retval['error_msg'] = elements[4].strip()
        return retval


    def parse_output(self, output):
            lines = output.split("\n")
            sections = []
            for i, line in enumerate(lines):
                if self.is_id_line(line):
                    sections.append(i)
            errors = []
            for i, line_pos in enumerate(sections):
                temp = self.parse_id_line(lines[line_pos])
                if i + 1 < len(sections):
                    temp['full_msg'] = "\n".join(lines[line_pos:sections[i + 1]])
                else:
                    temp['full_msg'] = "\n".join(lines[line_pos:])
                errors.append(temp)
            return errors


class GnuCompiler:
    def parse_output(self, output):
        return []
    
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
        results = self.compiler.parse_output(self.contents)
        if self.process.exitCode() == 0:
            self.compile_success.emit(results)
            self.write("[ Compilation Successful ]")
        else:
            self.compile_fail.emit(results)
        
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
        
