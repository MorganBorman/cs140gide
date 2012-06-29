from PyQt4 import QtCore
from PyQt4 import QtGui
import PyQt4.uic

class FloatingNotification(QtGui.QWidget):
    def __init__(self, parent=None, ui_file=None):
        QtGui.QWidget.__init__(self, parent)
        
        if ui_file is not None:
            PyQt4.uic.loadUi(ui_file, self)
        
        self.update_position()
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(32)
        self.timer.timeout.connect(self.update_position)
        #self.timer.start()
        
        self.setStyleSheet(self.STYLESHEET)
        
    STYLESHEET = '''
    #frame {
        color: rgb(0, 0, 0);
        background-color: rgb(200, 200, 200);
        border: 1px solid;
        border-color: rgb(100, 100, 100);
        border-radius: 5px;
        padding: 2px;
    }
    '''
        
    def update_position(self):
    
        if hasattr(self.parent(), 'viewport'):
            parentRect = self.parent().viewport().rect()
        else:
            parentRect = self.parent().rect()
            
        if not parentRect:
            return
            
        x = (parentRect.width()/2) - (self.width()/2)
        y = (parentRect.height()/2) - (self.height()/2)
        w = min(parentRect.width(), 268)
        
        self.setGeometry(x, y, w, self.height())
        
    def resizeEvent(self, event):
        self.update_position()
        
    def show(self):
        super(self.__class__, self).show()
        self.timer.start()
        
    def hide(self):
        super(self.__class__, self).hide()
        self.timer.stop()
