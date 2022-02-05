# import collections
import os
import glob
import subprocess

import clique
from package.constants import FFPROBE_PATH

class Movie():
    def __init__(self, filepath):
        ffprobe_path = FFPROBE_PATH.replace('/','\\')        
        filepath = filepath.replace('/','\\')
        
        ffprobe_seconds_cmd = f'{ffprobe_path} -v quiet -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 "{filepath}"'
        
        process_seconds = subprocess.Popen(ffprobe_seconds_cmd, shell=False, stdout=subprocess.PIPE)
        out, err = process_seconds.communicate()
        seconds = float(str(out).split("'")[1].split('\\')[0])
        
        ffprobe_fps_command = f'{ffprobe_path} -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate {filepath}'
        process_fps = subprocess.Popen(ffprobe_fps_command, shell=False, stdout=subprocess.PIPE)
        out, err = process_fps.communicate()
        fps = str(out).split("'")[1].split('\\')[0]
        fps = float(fps.split('/')[0]) / float(fps.split('/')[1])
        
        self.start = 1
        self.end = int(seconds * fps)
        self.shortname = os.path.basename(filepath)[:-4]
        self.folder = os.path.dirname(filepath).replace('\\','/')
        self.sourcepath = filepath
        self.seqtype = 'MOV'

       
class SequencesFromFiles():
    '''
    Returns a list of clique collections from a list of filepath in a common folder representing the file sequence these files are part of
    TO DO: need to adress missing files with a file sequence
    '''
    def __init__(self, filepath_list):
        self.filepath_list = filepath_list
        self.return_collections()

    def return_collections(self):
        filepath_list = [filepath for filepath in self.filepath_list if os.path.exists(filepath)]
        
        collections, remainder = clique.assemble(filepath_list)
       
        dir = os.path.dirname(filepath_list[0]) #assuming common folder, see if there is a need for files from multiple locations
        all_files_in_dir = glob.glob(f'{dir}\*')
        dir_collections, dir_remainder = clique.assemble(all_files_in_dir)
        dir_remainder = [remainder.replace("\\","/") for remainder in dir_remainder]

        self.selected_collections = []
        for dir_collection in dir_collections:
            for collection in collections:
                if collection.head.replace("\\","/") == dir_collection.head.replace("\\","/"):
                    self.add_properties(dir_collection)
                    self.selected_collections.append(dir_collection)
            for remainder_item in remainder:
                if remainder_item.startswith(dir_collection.head.replace("\\","/")) and remainder_item not in dir_remainder:
                    self.add_properties(dir_collection)
                    self.selected_collections.append(dir_collection)
                
        self.movs = []
        self.moviePath_list = [file for file in remainder if file.endswith('.mov')]
        if self.moviePath_list:
            for moviesPath in self.moviePath_list:
                movie = Movie(moviesPath)
                self.movs.append(movie)                
                    
    def add_properties(self, collection):
        collection.start = str(collection).split()[1].replace('[','').replace(']','').split('-')[0]
        collection.end = str(collection).split()[1].replace('[','').replace(']','').split('-')[1]

        shortname = os.path.basename(collection.head)
        folder =  os.path.dirname(collection.head)
        if shortname[-1] in ['.', '_']:
            shortname = shortname[:-1]
        collection.shortname = shortname
        collection.folder = folder
        collection.seqtype = 'IMG'
    
    @property
    def sequences(self):
        return self.selected_collections
    
    @property
    def movies(self):
        return self.movs

if __name__=='__main__':
    filepath_list = [r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\hyq010_All_bty_v018.1001.jpg',
                     r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\hyq010_All_bty_v018.1002.jpg',
                     r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\hyq010_All_bty_v018.1008.jpg',
                    #  r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\own470_l1_lin_v001.1016.jpg',
                    #  r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\own470_l1_lin_v001.1017.jpg',
                    #  r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\own470_l1_lin_v001.1040.jpg',
                     r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\own470_l1_lin_v001.10.jpg',
                     r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\pinup.jpg',
                     r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\dev010_lin_l1.1008.jpg',
                     r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\dev010_lin_l1.1022.jpg',]
                     
    sequences = SequencesFromFiles(filepath_list=filepath_list).sequences
    for seq in sequences:
        print(seq)