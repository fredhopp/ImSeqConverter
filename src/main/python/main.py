import sys
import os
import pathlib
import datetime
# import logging

from PySide6 import QtWidgets, QtGui

from package.main_window import MainWindow
import package.preferences as preferences 


# def logger():
#     filename_token = os.path.basename(sys.executable).split('.')[0]
#     date = datetime.datetime.now()
#     date_token = f'{date.year}{date.month}{date.day}_{date.hour}{date.minute}{date.second}'    
#     preferences.create_folder()
#     log_file_path = os.path.join(preferences.default_path(),f'{filename_token}_{date_token}.log')
    
#     # configure log formatter
#     logFormatter = logging.Formatter("%(asctime)s [%(filename)s] [%(funcName)s] [%(levelname)s] [%(lineno)d] %(message)s")
#     # configure file handler
#     fileHandler = logging.FileHandler(log_file_path)
#     fileHandler.setFormatter(logFormatter)
    
#     logger = logging.getLogger(__name__)
#     logger.addHandler(fileHandler)
    
#     # set the logging level
#     logger.setLevel(logging.DEBUG)
    
    
if __name__=='__main__':
    # main_logger = logger()
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

