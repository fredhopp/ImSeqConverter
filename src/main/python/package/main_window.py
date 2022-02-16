import os
# import logging
from functools import cached_property
from functools import partial

from PySide6 import QtGui, QtWidgets, QtCore

from package.worker import Worker
from package.file_sequence import SequencesFromFiles
import package.preferences as preferences


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, resource_dir):
        super().__init__()
        # self.sub_logger = logging.getLogger('__main__')
        self.resource_dir = resource_dir
        self.pref_window = None
        self.setWindowTitle('Image Sequence Converter')
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
        self.btn_add = QtWidgets.QPushButton()
        self.btn_selectAll = QtWidgets.QPushButton()
        self.btn_remove = QtWidgets.QPushButton()
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
        
        self.setAcceptDrops(True)
        self.lw_files.setAlternatingRowColors(True)
        self.lw_files.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        
        self.btn_add.setIcon(QtGui.QIcon(os.path.join(self.resource_dir, 'icons', 'plus.svg')))
        self.btn_add.setToolTip('Add image sequences or quicktimes to the list. (Drag & Drop)')
        self.btn_selectAll.setIcon(QtGui.QIcon(os.path.join(self.resource_dir, 'icons', 'select_all.svg')))
        self.btn_selectAll.setToolTip('Select all image sequences in the list. (Ctrl + A)')
        self.btn_remove.setIcon(QtGui.QIcon(os.path.join(self.resource_dir, 'icons', 'minus.svg')))
        self.btn_remove.setToolTip('Remove selected images sequences from the list. (Del)')
        
        self.lbl_outputSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.combo_colorspaceIn.addItem('ACEScg')
        self.combo_colorspaceIn.addItem('Utility - Linear - sRGB')
        self.combo_colorspaceIn.addItem('Output - sRGB')
        self.combo_colorspaceIn.addItem('Output - Rec.709')

        self.combo_colorspaceOut.addItem('Output - sRGB')
        self.combo_colorspaceOut.addItem('Output - Rec.709')
        self.combo_colorspaceOut.addItem('Utility - sRGB - Texture')
        
        self.combo_format.addItem('mp4 - h.264')
        self.combo_format.addItem('mp4 - h.265')
        self.combo_format.addItem('mov - prores')

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
        self.main_layout = QtWidgets.QGridLayout()
        self.centralWidget().setLayout(self.main_layout)

        self.left_layout = QtWidgets.QVBoxLayout()
        self.left_icon_layout = QtWidgets.QHBoxLayout()
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
        
        self.left_icon_layout.addWidget(self.btn_add)
        self.left_icon_layout.addWidget(self.btn_selectAll)
        self.left_icon_layout.addWidget(self.btn_remove)
        self.left_layout.addLayout(self.left_icon_layout)
        self.left_layout.addWidget(self.lw_files)
                
        # self.left_layout.addWidget(self.lbl_dropInfo)        
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
        self.btn_add.clicked.connect(self.pick_files)
        self.btn_selectAll.clicked.connect(self.select_all_items)
        self.btn_remove.clicked.connect(self.delete_selected_item)
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
            self.pref_window = preferences.PreferenceWindow()
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
                        
            selected_seqtype_values = list(set([item.seqtype for item in self.lw_files.selectedItems()]))
            
            if len(self.lw_files.selectedItems())==1:
                self.le_outputname.setDisabled(False)
                self.le_outputname.setText(list_item.outputname)
                if self.lw_files.selectedItems()[-1].seqtype == 'MOV':
                    # self.spn_head.setDisabled(True)
                    # self.spn_tail.setDisabled(True)
                    self.combo_fps.setDisabled(True)
            elif len(selected_seqtype_values)==1 and selected_seqtype_values[0]=='MOV': # all items are Quicktimes
                self.combo_fps.setDisabled(True)
                self.le_outputname.setDisabled(True)
            else:
                self.le_outputname.setDisabled(True)
                self.spn_head.setDisabled(False)
                self.spn_tail.setDisabled(False)
                self.combo_fps.setDisabled(False)
        else:
            self.enable_disable_attribute_widgets(True)

    def enable_disable_attribute_widgets(self, arg):
        self.le_outputname.setDisabled(arg)
        self.btn_outputFolder.setDisabled(arg)
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
            
    def select_all_items(self):
        lw_items = [self.lw_files.item(index) for index in range(self.lw_files.count())]
        for lw_item in lw_items:
            lw_item.setSelected(True)

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
        self.prg_dialog = QtWidgets.QProgressDialog('...', 'Cancel', 1, len(sequences_to_convert_boollist)+1)     
        self.prg_dialog.setWindowTitle('Encoding')
        self.prg_dialog.label =  QtWidgets.QLabel()
        self.prg_dialog.label.setAlignment(QtCore.Qt.AlignCenter)
        self.prg_dialog.setLabel(self.prg_dialog.label)
        self.prg_dialog.setValue(1) # needs to init
        self.prg_dialog.resize(320, 120)
        self.prg_dialog.canceled.connect(self.abort)
        self.prg_dialog.show()
        
        self.worker = Worker(lw_items, self.prg_dialog)
        # self.sub_logger.info(f'sent to worker: {self.worker.__dict__}')

        self.worker.moveToThread(self.thread)
        self.sub_logger.info('moved to thread')
        self.worker.signal_sequence_converted.connect(self.sequence_converted)
        self.thread.started.connect(self.worker.convert_sequences)
        self.thread.finished.connect(self.finish)
        # self.sub_logger.info('start thread')
        self.thread.start()       

    def abort(self):
        self.worker.runs = False
        self.thread.quit()
    
    def finish(self ):
        self.prg_dialog.setValue(self.prg_dialog.maximum())
        self.prg_dialog.cancel()
        self.thread.quit()
        file_progress_path = os.path.join(preferences.default_path(),'progress.buffer').replace('\\','/')
        if os.path.exists(file_progress_path):
            os.remove(file_progress_path)
        
    def signal_sequence_progress(self, lw_item, returned_value):
        pass
    
    def sequence_converted(self, lw_item, returned_value):
            if returned_value:
                lw_item.setIcon(self.cache_IconChecked)
                self.prg_dialog.setValue(self.prg_dialog.value() + 1) # TO DO: still does not update properly
                lw_item.processed = True
                self.thread.quit()            
                
    # Drag & Drop
    def dragEnterEvent(self, event):
        event.accept()

    def dragLeaveEvent(self, event):
        pass

    def dropEvent(self, event):
        if preferences.check():
            event.accept() # on animation enabled OS, the file would visually go back to the finder (OS UI animation)-> accept
            file_list = [url.toLocalFile() for url in event.mimeData().urls()]
            self.add_sequences(file_list)
        else:
            self.open_preferences('')
    
    def pick_files(self):
        if not preferences.check():
            self.open_preferences('')
        else:        
            default_folder = preferences.browse_load('last_location')
            if not os.path.isdir(default_folder):
                default_folder = os.path.expanduser('~')
            if file_list := QtWidgets.QFileDialog.getOpenFileNames(
                                                                    dir=default_folder,
                                                                    caption='Image Sequences or Quicktimes',
                                                                    # filter='Images (*.jpg *.JPG *.exr *.EXR)', # acceptance handled by file_sequence
                                                                ):
                last_location = os.path.dirname(file_list[0][0])
                preferences.browse_save('last_location', last_location)
                self.add_sequences(file_list[0])        
                
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
                lw_item.format = 'mp4 - h.264'
                
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