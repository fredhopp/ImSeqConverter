import os
from functools import cached_property
from functools import partial

from PySide6 import QtGui, QtWidgets, QtCore

from package.worker import Worker
from package.file_sequence import SequencesFromFiles
from package.preferences_window import PreferenceWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, resource_dir):
        super().__init__()
        self.resource_dir = resource_dir
        self.pref_window = None
        self.setWindowTitle('Movie Converter')
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.central_widget =  QtWidgets.QWidget()               # define central widget
        self.setCentralWidget(self.central_widget)
        
        self.lw_files = QtWidgets.QListWidget()
        self.lbl_dropInfo = QtWidgets.QLabel('Drop images on above UI')
        self.btn_convert = QtWidgets.QPushButton('Convert')
        self.color_blue = QtGui.QColor(237,247,247)
        self.color_green = QtGui.QColor(200,237,172)

        self.lbl_outputSettings = QtWidgets.QLabel('Output Settings')
        self.le_outputname = QtWidgets.QLineEdit('Filename')
        self.combo_format = QtWidgets.QComboBox()
        
        self.combo_colorspaceIn = QtWidgets.QComboBox()
        self.combo_colorspaceOut = QtWidgets.QComboBox()

        self.spn_head = QtWidgets.QSpinBox()
        self.spn_tail = QtWidgets.QSpinBox()
        
        self.combo_fps = QtWidgets.QComboBox()
        self.combo_quality = QtWidgets.QComboBox()
        self.combo_resolution = QtWidgets.QComboBox()

        self.check_framenum = QtWidgets.QCheckBox()

        self.btn_outputFolder = QtWidgets.QPushButton()
        self.le_outputFolder = QtWidgets.QLineEdit('Ouput Folder')
            
    def modify_widgets(self):
        self.preference_action = QtGui.QAction( "&Open", self)
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&Preferences")
        file_menu.addAction(self.preference_action)
        
        self.lbl_dropInfo.setVisible(False)
        self.setAcceptDrops(True)
        self.lw_files.setAlternatingRowColors(True)
        self.lw_files.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)

        self.lbl_outputSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.combo_colorspaceIn.addItem('ACEScg')
        self.combo_colorspaceIn.addItem('Utility - Linear - sRGB')
        self.combo_colorspaceIn.addItem('Output - sRGB')
        self.combo_colorspaceIn.addItem('Output - Rec.709')

        self.combo_colorspaceOut.addItem('Output - sRGB')
        self.combo_colorspaceOut.addItem('Output - Rec.709')
        self.combo_colorspaceOut.addItem('Utility - sRGB - Texture')
        
        self.combo_format.addItem('mp4')
        self.combo_format.addItem('prores-mov')

        self.combo_fps.addItem('23.976')
        self.combo_fps.addItem('24')
        self.combo_fps.addItem('25')
        self.combo_fps.addItem('29.97')
        self.combo_fps.addItem('30')

        self.combo_quality.addItem('High')
        self.combo_quality.addItem('Medium')
        self.combo_quality.addItem('Low')       
        
        self.combo_resolution.addItem('Original')
        self.combo_resolution.addItem('1080p')
        self.combo_resolution.addItem('UHD')

        self.spn_head.setRange(0,100)
        self.spn_tail.setRange(0,100)
       
        self.btn_outputFolder.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogOpenButton')))
        self.le_outputFolder.setText('Output Folder...')

        self.update_properties_display()
        
    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)
        self.centralWidget().setLayout(self.main_layout)

        self.left_layout = QtWidgets.QVBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()        
        
        self.right_title_layout = QtWidgets.QHBoxLayout()
        self.right_form_layout = QtWidgets.QFormLayout()
        self.right_folder_layout = QtWidgets.QHBoxLayout()
        
    def add_widgets_to_layouts(self):
        self.main_layout.addLayout(self.left_layout,0,0,1,1)
        self.main_layout.addLayout(self.right_layout,0,1,1,1)
                
        self.right_layout.addLayout(self.right_title_layout)
        self.right_layout.addLayout(self.right_form_layout)
        self.right_layout.addStretch()
        self.right_layout.addLayout(self.right_folder_layout)
        
        self.left_layout.addWidget(self.lw_files)
        self.left_layout.addWidget(self.lbl_dropInfo)
        
        self.main_layout.addWidget(self.btn_convert, 1, 0, 1, 2)
        
        self.right_title_layout.addWidget(self.lbl_outputSettings)
        
        self.right_form_layout.addRow('Filename',self.le_outputname)
        self.right_form_layout.addRow('Format',self.combo_format)
        self.right_form_layout.addRow('Input Colorspace',self.combo_colorspaceIn)
        self.right_form_layout.addRow('Output Colorspace',self.combo_colorspaceOut)
        self.right_form_layout.addRow('Quality',self.combo_quality)
        self.right_form_layout.addRow('Fps',self.combo_fps)
        self.right_form_layout.addRow('Resolution',self.combo_resolution)
        self.right_form_layout.addRow('Trim Head',self.spn_head)
        self.right_form_layout.addRow('Trim Tail',self.spn_tail)
        self.right_form_layout.addRow('Overlay Frame Number',self.check_framenum)

        self.right_folder_layout.addWidget(self.btn_outputFolder)
        self.right_folder_layout.addWidget(self.le_outputFolder)
        
    def setup_connections(self):
        QtGui.QShortcut(QtGui.QKeySequence('Delete'), self.lw_files, self.delete_selected_item)
        self.preference_action.triggered.connect(self.open_preferences)
        self.lw_files.itemSelectionChanged.connect(self.update_properties_display)
        self.le_outputname.textChanged.connect(partial(self.update_sequence_attribute, 'outputname', self.le_outputname.text()))
        self.combo_format.currentTextChanged.connect(partial(self.update_sequence_attribute, 'format', self.combo_format.currentText()))
        self.combo_quality.currentTextChanged.connect(partial(self.update_sequence_attribute, 'quality', self.combo_quality.currentText()))
        self.combo_colorspaceIn.currentTextChanged.connect(partial(self.update_sequence_attribute, 'colorspaceIn', self.combo_quality.currentText()))
        self.combo_colorspaceOut.currentTextChanged.connect(partial(self.update_sequence_attribute, 'colorspaceOut', self.combo_quality.currentText()))
        self.combo_fps.currentTextChanged.connect(partial(self.update_sequence_attribute, 'fps', self.combo_fps.currentText()))
        self.combo_resolution.currentTextChanged.connect(partial(self.update_sequence_attribute, 'resolution', self.combo_resolution.currentText()))
        self.spn_head.valueChanged.connect(partial(self.update_sequence_attribute, 'head', self.spn_head.value()))
        self.spn_tail.valueChanged.connect(partial(self.update_sequence_attribute, 'tail', self.spn_tail.value()))
        self.check_framenum.stateChanged.connect(partial(self.update_sequence_attribute, 'ovl_framenum', self.check_framenum.isChecked()))
        self.btn_outputFolder.clicked.connect(self.pick_folder)
        self.le_outputFolder.textChanged.connect(partial(self.update_sequence_attribute, 'outputfolder', self.le_outputFolder.text()))

        self.btn_convert.clicked.connect(self.convert_sequences)
   
    def pick_folder(self):
        defaultfolder = self.le_outputFolder.text()
        if not os.path.isdir(defaultfolder):
            defaultfolder = os.path.expanduser('~')
        if folder := QtWidgets.QFileDialog.getExistingDirectory(
                                                                dir=defaultfolder,
                                                                caption='Output Folder',
                                                                options=QtWidgets.QFileDialog.ShowDirsOnly,
                                                            ):
            self.le_outputFolder.setText(folder)

    def open_preferences(self, checked):
        if self.pref_window is None:
            self.pref_window = PreferenceWindow()
        self.pref_window.show()

    def update_sequence_attribute(self, attribute, connect_item, attrib_value ):
        # sourcery skip: use-named-expression
        list_items = self.lw_files.selectedItems()
        if list_items:
            for list_item in list_items:
                if isinstance(attrib_value, str) and (
                                                    not attrib_value.startswith('"')
                                                    or not attrib_value.endswith('"')
                                                    ): 
                    attrib_value = f'"{attrib_value}"'
                command = f'list_item.{attribute} = {attrib_value}'
                exec(command)

    def update_properties_display(self):
        if self.lw_files.selectedItems():
            self.enable_disable_attribute_widgets(False)
            list_item = self.lw_files.selectedItems()[-1]
            self.le_outputFolder.setText(list_item.outputfolder)
            self.combo_colorspaceIn.setCurrentText(list_item.colorspaceIn)
            self.combo_colorspaceOut.setCurrentText(list_item.colorspaceOut)
            self.spn_head.setValue(list_item.head)
            self.spn_tail.setValue(list_item.tail)
            self.combo_quality.setCurrentText(list_item.quality)
            self.combo_format.setCurrentText(list_item.format)
            self.combo_fps.setCurrentText(list_item.fps)
            self.check_framenum.setChecked(list_item.ovl_framenum)
            self.combo_resolution.setCurrentText(list_item.resolution)

            if len(self.lw_files.selectedItems())==1:
                self.le_outputname.setDisabled(False)
                self.le_outputname.setText(list_item.outputname)
                if self.lw_files.selectedItems()[-1].seqtype == 'MOV':
                    # self.spn_head.setDisabled(True)
                    # self.spn_tail.setDisabled(True)
                    self.combo_fps.setDisabled(True)
            else:
                self.le_outputname.setDisabled(True)
                self.spn_head.setDisabled(False)
                self.spn_tail.setDisabled(False)
                self.combo_fps.setDisabled(False)
        else:
            self.enable_disable_attribute_widgets(True)

    def enable_disable_attribute_widgets(self, arg):
        self.le_outputname.setDisabled(arg)
        self.le_outputFolder.setDisabled(arg)
        
        self.combo_quality.setDisabled(arg)
        self.combo_format.setDisabled(arg)
        
        self.combo_colorspaceIn.setDisabled(arg)
        self.combo_colorspaceOut.setDisabled(arg)
        self.check_framenum.setDisabled(arg)
        self.combo_resolution.setDisabled(arg)

        self.spn_head.setDisabled(arg)
        self.spn_tail.setDisabled(arg)
        self.combo_fps.setDisabled(arg)
            
    def delete_selected_item(self):
        for lw_item in self.lw_files.selectedItems():
            self.lw_files.takeItem(self.lw_files.row(lw_item))

    def convert_sequences(self):
        lw_items = [self.lw_files.item(index) for index in range(self.lw_files.count())]
        sequences_to_convert_boollist = [True for lw_item in lw_items if not lw_item.processed]
        if not sequences_to_convert_boollist:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                'No Sequences to convert',
                                'All sequences have been converted')
            msg_box.exec_()
            return False

        self.thread = QtCore.QThread(self)

        self.worker = Worker(lw_items)

        self.worker.moveToThread(self.thread)
        self.worker.signal_sequence_converted.connect(self.sequence_converted)
        self.thread.started.connect(self.worker.convert_sequences)
        self.thread.finished.connect(self.finish)

        self.thread.start()
        
        self.prg_dialog = QtWidgets.QProgressDialog('Movie Conversion', 'Cancel', 1, len(sequences_to_convert_boollist))
        self.prg_dialog.canceled.connect(self.abort)
        self.prg_dialog.show()

    def abort(self):
        self.worker.runs = False
        self.thread.quit()
    
    def finish(self ):
        self.prg_dialog.setValue(self.prg_dialog.maximum())
        self.prg_dialog.cancel()
        self.thread.quit()

    def sequence_converted(self, lw_item, returned_value):
            if returned_value:
                lw_item.setIcon(self.cache_IconChecked)
                self.prg_dialog.setValue(self.prg_dialog.value() + 1) # TO DO: still does not update properly
                lw_item.processed = True
                self.thread.quit()
                
    # Drag & Drop
    def dragEnterEvent(self, event):
        self.lbl_dropInfo.setVisible(True)
        event.accept()

    def dragLeaveEvent(self, event):
        self.lbl_dropInfo.setVisible(False)

    def dropEvent(self, event):
        event.accept() # on animation enabled OS, the file would visually go back to thge finder (OS UI animation)-> accept

        file_list = [url.toLocalFile() for url in event.mimeData().urls()]

        self.add_sequences(file_list)
        self.lbl_dropInfo.setVisible(False)

    def add_sequences(self, file_list):
        sqff = SequencesFromFiles(filepath_list=file_list)
        seqs = sqff.sequences
        movs = sqff.movies
        seqs.extend(movs)
        
        lw_item_texts = [f'{self.lw_files.item(index).text()}' for index in range(self.lw_files.count())]
         
        for seq in seqs:
            lw_item_text = f'{seq.shortname} [{seq.start}-{seq.end}] ({seq.seqtype})'
            if lw_item_text not in lw_item_texts:
                lw_item = QtWidgets.QListWidgetItem(lw_item_text)
                lw_item.setIcon(self.cache_IconUnChecked)
                lw_item.setBackground(self.color_blue)
                lw_item.processed = False
                self.lw_files.addItem(lw_item)
                lw_item.shortname = seq.shortname
                lw_item.outputname = seq.shortname
                lw_item.folder = seq.folder
                lw_item.outputfolder = seq.folder
                lw_item.start = seq.start
                lw_item.end = seq.end
                lw_item.head = 0
                lw_item.tail = 0
                lw_item.format = 'mp4'
                
                lw_item.quality = 'High'
                lw_item.colorspaceIn = 'ACEScg'
                lw_item.colorspaceOut = 'Output - sRGB'
                lw_item.ovl_framenum = False
                lw_item.resolution = 'Original'
                lw_item.seqtype = seq.seqtype
                
                if lw_item.seqtype == 'IMG':
                    padding_str = f'%0{seq.padding}d'
                    if seq.padding==0:
                        padding_str = '%d'
                    lw_item.sourcepath = f'{seq.head}{padding_str}{seq.tail}'
                    lw_item.fps = '23.976'
                else: # lw_item.seqtype == 'MOV':
                    lw_item.sourcepath = seq.sourcepath
                    lw_item.fps = str(seq.fps)

    @cached_property
    def cache_IconChecked(self):
        return QtGui.QIcon(os.path.join(self.resource_dir, 'icons', 'checked.svg'))

    @cached_property
    def cache_IconUnChecked(self):
        return QtGui.QIcon(os.path.join(self.resource_dir, 'icons', 'unchecked.svg'))