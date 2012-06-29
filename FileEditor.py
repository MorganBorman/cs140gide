from PyQt4 import Qsci
from PyQt4 import QtGui

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
