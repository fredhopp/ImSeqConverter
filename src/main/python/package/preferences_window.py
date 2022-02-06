import os
import json

from functools import partial
from PySide6 import QtWidgets

class PreferenceWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 250)
        self.setWindowTitle('Preferences')
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.load_preferences()
        
    def create_widgets(self):
        self.lbl_ffmpeg_link_description = QtWidgets.QLabel('ffmpeg download link:')
        self.lbl_ffmpeg_link = QtWidgets.QLabel('https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z')
        self.bt_ffmpeg_website = QtWidgets.QPushButton('Copy Download Link')
        
        self.lbl_ffmpegDir = QtWidgets.QLabel('ffmpeg folder:')
        self.btn_ffmpegDir = QtWidgets.QPushButton()
        self.le_ffmpegDir = QtWidgets.QLineEdit('Path to ffmpeg executable')
        
        self.lbl_font = QtWidgets.QLabel('Font used for frame overlay:')
        self.btn_font = QtWidgets.QPushButton()
        self.le_font = QtWidgets.QLineEdit('Path to font')
        
        self.lbl_lutDir = QtWidgets.QLabel('Colospace Luts folder:')
        self.btn_lutDir = QtWidgets.QPushButton()
        self.le_lutDir = QtWidgets.QLineEdit('Path to Colospace Luts folder')
        
        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_save = QtWidgets.QPushButton('Save Preferences')
    
    def modify_widgets(self):
        self.btn_ffmpegDir.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogOpenButton')))
        self.btn_font.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogOpenButton')))
        self.btn_lutDir.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogOpenButton')))

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)        
        self.ffmpegUrl_layout = QtWidgets.QHBoxLayout()
        self.ffmpegExe_layout = QtWidgets.QHBoxLayout()           
        self.font_layout = QtWidgets.QHBoxLayout()
        self.lut_layout = QtWidgets.QHBoxLayout()
        self.savecancel_layout = QtWidgets.QHBoxLayout()

    def add_widgets_to_layouts(self):
        self.main_layout.addLayout(self.ffmpegUrl_layout)
        self.main_layout.addStretch()
        
        self.main_layout.addWidget(self.lbl_ffmpegDir)
        self.main_layout.addLayout(self.ffmpegExe_layout)
        
        self.main_layout.addWidget(self.lbl_font)
        self.main_layout.addLayout(self.font_layout)
        
        self.main_layout.addWidget(self.lbl_lutDir)
        self.main_layout.addLayout(self.lut_layout)
        
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.savecancel_layout)
        
        self.ffmpegUrl_layout.addWidget(self.lbl_ffmpeg_link_description)
        self.ffmpegUrl_layout.addStretch()
        self.ffmpegUrl_layout.addWidget(self.lbl_ffmpeg_link)
        self.ffmpegUrl_layout.addStretch()
        self.ffmpegUrl_layout.addWidget(self.bt_ffmpeg_website)
        
        self.ffmpegExe_layout.addWidget(self.le_ffmpegDir)
        self.ffmpegExe_layout.addWidget(self.btn_ffmpegDir)
        
        self.font_layout.addWidget(self.le_font)
        self.font_layout.addWidget(self.btn_font)
        
        self.lut_layout.addWidget(self.le_lutDir)
        self.lut_layout.addWidget(self.btn_lutDir)
        
        self.savecancel_layout.addStretch()
        self.savecancel_layout.addWidget(self.btn_cancel)
        self.savecancel_layout.addWidget(self.btn_save)

    def setup_connections(self):
        self.bt_ffmpeg_website.clicked.connect(partial(self.copy_string,'https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z'))
        self.btn_ffmpegDir.clicked.connect(self.pick_ffmpeg_folder)
        self.btn_font.clicked.connect(partial(self.pick_font))
        self.btn_lutDir.clicked.connect(partial(self.pick_lut_folder))
        self.btn_save.clicked.connect(partial(self.save_preferences))
        self.btn_cancel.clicked.connect(partial(self.close_preference_window))

    def copy_string(self, str):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(str)
        
    def pick_ffmpeg_folder(self):
        default_folder = self.le_ffmpegDir.text()
        if not os.path.isdir(default_folder):
            default_folder = os.path.expanduser('~')
        if folder := QtWidgets.QFileDialog.getExistingDirectory(
                                                                dir=default_folder,
                                                                caption='ffmpeg Folder',
                                                                options=QtWidgets.QFileDialog.ShowDirsOnly,
                                                                ):
            self.le_ffmpegDir.setText(folder)
            
    def pick_lut_folder(self):
        default_folder = self.le_lutDir.text()
        if not os.path.isdir(default_folder):
            default_folder = os.path.expanduser('~')
        if folder := QtWidgets.QFileDialog.getExistingDirectory(
                                                                dir=default_folder,
                                                                caption='Colorspace Luts Folder',
                                                                options=QtWidgets.QFileDialog.ShowDirsOnly,
                                                                ):
            self.le_lutDir.setText(folder)
    
    def pick_font(self):
        default_file = self.le_font.text()
        default_folder = os.path.dirname(default_file)
        if not os.path.exists(default_folder):
            default_folder = os.path.expanduser('~')
        if font_file := QtWidgets.QFileDialog.getOpenFileName(
                                                                dir=default_folder,
                                                                caption='Font',
                                                                filter='Fonts (*.ttf)',
                                                            ):
            self.le_font.setText(font_file[0].replace('\\','/'))
            
    def load_preferences(self):
        user_dir = os.path.expanduser('~')
        pref_dir = os.path.join(user_dir,'.ImageSequenceConverter')
        pref_file = os.path.join(pref_dir,'preferences.json')

        if os.path.exists(pref_file):
            with open(pref_file, 'r') as pref_file:
                json_object = json.load(pref_file)
                for key, value in json_object.items():
                    if key == 'ffmpeg_dir':
                        self.le_ffmpegDir.setText(value.replace('\\','/'))
                    if key == 'font_file':
                        self.le_font.setText(value.replace('\\','/'))
                    if key == 'lut_dir':
                        self.le_lutDir.setText(value.replace('\\','/'))
                        
    def save_preferences(self):
        user_dir = os.path.expanduser('~')
        pref_dir = os.path.join(user_dir,'.ImageSequenceConverter')
        if not os.path.exists(pref_dir):
            os.mkdir(pref_dir)
        pref_file = os.path.join(pref_dir,'preferences.json')
        
        if (os.path.isdir(self.le_ffmpegDir.text()) and os.path.isdir(self.le_lutDir.text()) and os.path.exists(self.le_font.text()) and self.le_font.text().endswith('.ttf')): #
            pref_dic = {
                        'ffmpeg_dir': self.le_ffmpegDir.text().replace('\\','/'),
                        'font_file': self.le_font.text().replace('\\','/'),
                        'lut_dir': self.le_lutDir.text().replace('\\','/'),
                        }
            json_object = json.dumps(pref_dic, indent=4)

            with open(pref_file, 'w') as pref_file:
                pref_file.write(json_object)
            self.close_preference_window()
        else:
            self.warning_dialog('Choose a valid folder for ffmpeg, colospace luts and a font file')
            
    def warning_dialog(self, message):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle('Warning')
        dlg.setText(message)
        button = dlg.exec_()
            
    def close_preference_window(self):
        self.close()