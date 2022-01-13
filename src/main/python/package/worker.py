from PySide6 import QtCore

from package.convert import ConvertToMovie

class Worker(QtCore.QObject):
    image_converted = QtCore.Signal(object, bool)
    finished = QtCore.Signal()
    
    def __init__(self, image_sequences, folder):
        super().__init__()
        self.image_sequences = image_sequences
        self.folder = folder
        self.runs = True
    
    def convert_images(self):
        for sequence_lw_item in self.image_sequences:
            if self.runs and not sequence_lw_item.processed:
                movie = ConvertToMovie(path=sequence_lw_item.text(), folder=self.folder)
                success = movie.to_mp4(size=self.size, quality=self.quality)
                self.image_converted.emit(sequence_lw_item, success)

        self.finished.emit()