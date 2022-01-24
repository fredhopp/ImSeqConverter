import os
from functools import cached_property
from functools import partial

from PySide6 import QtGui, QtWidgets, QtCore

from package.worker import Worker
from package.file_sequence import SequencesFromFiles


class MainWindow(QtWidgets.QWidget):
    def __init__(self, resource_dir):
        super().__init__()
        self.resource_dir = resource_dir
        self.setWindowTitle('Movie Converter')
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.lw_files = QtWidgets.QListWidget()
        self.lbl_dropInfo = QtWidgets.QLabel('Drop images on above UI')
        self.btn_convert = QtWidgets.QPushButton('Convert')
        self.color_blue = QtGui.QColor(237,247,247)
        self.color_green = QtGui.QColor(200,237,172)

        self.le_outputname = QtWidgets.QLineEdit('Filename')

        self.spn_head = QtWidgets.QSpinBox()
        self.spn_tail = QtWidgets.QSpinBox()

        self.combo_format = QtWidgets.QComboBox()
        self.combo_fps = QtWidgets.QComboBox()

        self.btn_outputFolder = QtWidgets.QPushButton()
        self.le_outputFolder = QtWidgets.QLineEdit('Ouput Folder')
            
    def modify_widgets(self):
        self.lbl_dropInfo.setVisible(False)
        self.setAcceptDrops(True)
        self.lw_files.setAlternatingRowColors(True)
        self.lw_files.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)

        self.combo_format.addItem('mp4')
        self.combo_format.addItem('mov')

        self.combo_fps.addItem('23.976')
        self.combo_fps.addItem('24')
        self.combo_fps.addItem('25')
        self.combo_fps.addItem('29.97')
        self.combo_fps.addItem('30')

        self.spn_head.setRange(0,100)
        self.spn_tail.setRange(0,100)
        
        self.btn_outputFolder.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogOpenButton')))
        self.le_outputFolder.setText('Output Folder...')
        
    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

        self.left_layout = QtWidgets.QGridLayout()        

        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_form_layout = QtWidgets.QFormLayout()
        self.right_folder_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addLayout(self.left_layout,0,0,1,1)
        self.main_layout.addLayout(self.right_layout,0,1,1,1)
        self.right_layout.addLayout(self.right_form_layout)
        self.right_layout.addLayout(self.right_folder_layout)
        
    def add_widgets_to_layouts(self):
        self.left_layout.addWidget(self.lw_files, 0, 0, 1, 2)
        self.left_layout.addWidget(self.lbl_dropInfo, 1, 0, 1, 2)
        self.main_layout.addWidget(self.btn_convert, 1, 0, 1, 2)

        self.right_form_layout.addRow('Filename',self.le_outputname)
        self.right_form_layout.addRow('Format',self.combo_format)
        self.right_form_layout.addRow('fps',self.combo_fps)
        self.right_form_layout.addRow('Trim Head',self.spn_head)
        self.right_form_layout.addRow('Trim Tail',self.spn_tail)
        self.right_folder_layout.addWidget(self.btn_outputFolder)
        self.right_folder_layout.addWidget(self.le_outputFolder)
        
    def setup_connections(self):
        QtGui.QShortcut(QtGui.QKeySequence('Delete'), self.lw_files, self.delete_selected_item)
        self.lw_files.itemSelectionChanged.connect(self.update_properties_display)
        self.le_outputname.textChanged.connect(partial(self.update_sequence_attribute, 'outputname', self.le_outputname.text()))
        self.combo_format.currentTextChanged.connect(partial(self.update_sequence_attribute, 'format', self.combo_format.currentText()))
        self.combo_fps.currentTextChanged.connect(partial(self.update_sequence_attribute, 'fps', self.combo_fps.currentText()))
        self.spn_head.valueChanged.connect(partial(self.update_sequence_attribute, 'head', self.spn_head.value()))
        self.spn_tail.valueChanged.connect(partial(self.update_sequence_attribute, 'tail', self.spn_head.value()))
        self.btn_outputFolder.clicked.connect(self.pick_folder)
        self.le_outputFolder.textChanged.connect(partial(self.update_sequence_attribute, 'outputfolder', self.le_outputFolder.text()))

        self.btn_convert.clicked.connect(self.convert_sequences)
    
    def pick_folder(self):
        defaultfolder = self.le_outputFolder.text()
        if not os.path.isdir(defaultfolder):
            defaultfolder = os.path.expanduser('~')
        folder = QtWidgets.QFileDialog.getExistingDirectory(dir=defaultfolder, caption='Output Folder',options=QtWidgets.QFileDialog.ShowDirsOnly)
        if folder:
            self.le_outputFolder.setText(folder)

    def update_sequence_attribute(self, attribute, connect_item, attrib_value ):
        # print(f'{attribute} - {attrib_value} - {connect_item}')
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
            list_item = self.lw_files.selectedItems()[-1]
            self.le_outputname.setText(list_item.outputname)
            self.le_outputFolder.setText(list_item.outputfolder)
            self.spn_head.setValue(list_item.head)
            self.spn_tail.setValue(list_item.tail)
            self.combo_format.setCurrentText(list_item.format)
            self.combo_fps.setCurrentText(list_item.fps)

    def convert_sequences(self):
        lw_items = [self.lw_files.item(index) for index in range(self.lw_files.count())]
        sequences_to_convert_boollist = [True for lw_item in lw_items if not lw_item.processed]
        if not sequences_to_convert_boollist:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                'No image to process',
                                'All images have been processed')
            msg_box.exec_()
            return False

        self.thread = QtCore.QThread(self)

        self.worker = Worker(lw_items)

        self.worker.moveToThread(self.thread)
        self.worker.signal_sequence_converted.connect(self.sequence_converted)
        self.thread.started.connect(self.worker.convert_sequences)
        self.thread.finished.connect(self.thread.quit)
        self.thread.start()

        self.prg_dialog = QtWidgets.QProgressDialog('Movie Conversion', 'Cancel', 1, len(sequences_to_convert_boollist))
        self.prg_dialog.canceled.connect(self.abort)
        self.prg_dialog.show()

    def abort(self):
        self.worker.runs = False
        self.thread.quit()

    def sequence_converted(self, lw_item, success):
            if success:
                lw_item.setIcon(self.cache_IconChecked)
                lw_item.processed = True
                self.prg_dialog.setValue(self.prg_dialog.value() + 1)
        
    def delete_selected_item(self):
        for lw_item in self.lw_files.selectedItems():
            self.lw_files.takeItem(self.lw_files.row(lw_item))

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
        seqs = SequencesFromFiles(filepath_list=file_list).sequences
        items = [self.lw_files.item(index).shortname for index in range(self.lw_files.count())]
         
        for seq in seqs:
            if seq.shortname not in items:
                lw_item = QtWidgets.QListWidgetItem(f'{seq.shortname} ({seq.start}-{seq.end})')
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
                lw_item.fps = '23.976'
                padding_str = f'%0{seq.padding}d'
                if seq.padding==0:
                    padding_str = '%d'
                lw_item.sourcepath = f'{seq.head}{padding_str}{seq.tail}'

    @cached_property
    def cache_IconChecked(self):
        return QtGui.QIcon(os.path.join(self.resource_dir, 'icons', 'checked.svg'))

    @cached_property
    def cache_IconUnChecked(self):
        return QtGui.QIcon(os.path.join(self.resource_dir, 'icons', 'unchecked.svg'))