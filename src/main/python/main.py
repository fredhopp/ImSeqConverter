from package.main_window import MainWindow
from PySide6.QtWidgets import QApplication

import sys
import os
import pathlib

if __name__=='__main__':
    app = QApplication(sys.argv)
    resource_dir = os.path.join(pathlib.Path(__file__).parent.parent.absolute(),'resources' )
    window = MainWindow(resource_dir=resource_dir)
    # window = MainWindow()
    window.resize(1920/4, 1200/2)
    window.show()
    sys.exit(app.exec())
