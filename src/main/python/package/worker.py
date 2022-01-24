from PySide6 import QtCore

from package.convert import ConvertToMovie

class Worker(QtCore.QObject):
    signal_sequence_converted = QtCore.Signal(object, bool)
    finished = QtCore.Signal()
    
    def __init__(self, lw_items):
        super().__init__()
        self.lw_items = lw_items
        self.runs = True
    
    def convert_sequences(self):
        for lw_item in self.lw_items:
            if self.runs and not lw_item.processed:
                startframe = int(lw_item.start) + int(lw_item.head)
                framerange = int(lw_item.end) - int(lw_item.start) - ( int(lw_item.head) + int(lw_item.tail))
                movie = ConvertToMovie(sourcepath=lw_item.sourcepath,
                                        filename=lw_item.outputname,
                                        format=lw_item.format,
                                        fps=lw_item.fps,
                                        startframe = startframe,
                                        framerange = framerange,
                                        outputfolder = lw_item.outputfolder
                                        )
                
                success = movie.to_movie()
                self.signal_sequence_converted.emit(lw_item, success)

        self.finished.emit()