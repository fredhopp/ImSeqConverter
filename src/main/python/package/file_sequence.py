import os
import glob
import subprocess
import json

import clique

import package.preferences as preferences
     
def find_ffprobe():  # sourcery skip: merge-nested-ifs
    pref_dir = preferences.default_path()
    pref_file = os.path.join(pref_dir,'preferences.json')

    FFPROBE_PATH = None
    if os.path.exists(pref_file):
        with open(pref_file, 'r') as pref_file:
            json_object = json.load(pref_file)
            for key, value in json_object.items():
                if key == 'ffmpeg_dir':
                    FFPROBE_PATH = os.path.join(value,'ffprobe.exe').replace('/','\\')
    if FFPROBE_PATH:
        if os.path.exists(FFPROBE_PATH) and FFPROBE_PATH.endswith('ffprobe.exe'):
            return FFPROBE_PATH

class Movie():
    def __init__(self, filepath):
        ffprobe_path = find_ffprobe()
        filepath = filepath.replace('/','\\')
        
        ffprobe_seconds_cmd = (f'{ffprobe_path} -v quiet -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 ' 
                               r'"' # splitting to be able to "over"-quote for ffprobe
                               f'{filepath}'
                               r'"'
                            )
        process_seconds = subprocess.Popen(ffprobe_seconds_cmd, shell=False, stdout=subprocess.PIPE)
        out, err = process_seconds.communicate()
        seconds = float(str(out).split("'")[1].split('\\')[0])
        
        ffprobe_fps_command = (f'{ffprobe_path} -v quiet -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate ' 
                               r'"' # splitting to be able to "over"-quote for ffprobe
                               f'{filepath}'
                               r'"'
                            )
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
        self.fps = fps
 
class SequencesFromFiles():
    '''
    Returns a list of clique collections from a list of filepath in a common folder representing the file sequence these files are part of
    TO DO: need to adress missing files with a file sequence
    '''
    def __init__(self, filepath_list):
        self.filepath_list = filepath_list
        self.return_sequences()
                        
    def return_sequences(self):  # sourcery skip: extract-method
        imSequence_extensions = ['jpg','jpeg','png','tif','tiff','exr','dpx','tga']
        movie_extensions = ['mov','avi','mkv','mp4']
        imSequence_extensions.append([ext.upper() for ext in imSequence_extensions ])
        movie_extensions.append([ext.upper() for ext in movie_extensions ])
        imageFilePath_list = []
        movieFilePath_list = []
        
        for imageFilePath in self.filepath_list:
            for ext in imSequence_extensions:
                if imageFilePath.endswith(f'.{ext}'):
                    imageFilePath_list.append(imageFilePath)
                    break    
            for ext in movie_extensions:
                if imageFilePath.endswith(f'.{ext}'):
                    movieFilePath_list.append(imageFilePath)
                    break
        
        self.imSequences = []
        if imageFilePath_list:
            collections, remainder = clique.assemble(imageFilePath_list)
            dir = os.path.dirname(imageFilePath_list[0]) #assuming common folder, see if there is a need for files from multiple locations
            all_files_in_dir = glob.glob(f'{dir}\*')
            dir_collections, dir_remainder = clique.assemble(all_files_in_dir)
            dir_remainder = [remainder.replace("\\","/") for remainder in dir_remainder]

            for dir_collection in dir_collections:
                for collection in collections:
                    if collection.head.replace("\\","/") == dir_collection.head.replace("\\","/"):
                        if  collection.tail == dir_collection.tail:
                            self.add_properties(dir_collection)
                            self.imSequences.append(dir_collection)
                for remainder_item in remainder:
                    if remainder_item.startswith(dir_collection.head.replace("\\","/")) and remainder_item not in dir_remainder:
                        if remainder_item.endswith(dir_collection.tail):
                            self.add_properties(dir_collection)
                            self.imSequences.append(dir_collection)
                
        self.movs = []
        if movieFilePath_list:
            for movieFilePath in movieFilePath_list:
                movie = Movie(movieFilePath)
                self.movs.append(movie)            
                
        # print(f'filepathList: {self.filepath_list}\nmovs: {self.movs}\nimSequences: {self.imSequences}')
                    
    def add_properties(self, collection):
        collection.start = str(collection).split()[1].replace('[','').replace(']','').split('-')[0]
        # BREAKS IF SPACE IN NAME, index out of list or something !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        return self.imSequences
    
    @property
    def movies(self):
        return self.movs
