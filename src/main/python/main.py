import sys
import os
import pathlib

from PySide6 import QtWidgets, QtGui

from package.main_window import MainWindow

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        resource_dir = sys._MEIPASS
    else:
        resource_dir = os.path.join(pathlib.Path(__file__).parent.parent.absolute(),'resources' )
    
    app_icon_path = os.path.join(resource_dir,'icons','ImSeqConverter.ico')
    
    window = MainWindow(resource_dir=resource_dir)
    
    window.resize(640, 480)
    window.show()
    app.setWindowIcon(QtGui.QIcon(app_icon_path))
    window.setWindowIcon(QtGui.QIcon(app_icon_path))
    sys.exit(app.exec())

