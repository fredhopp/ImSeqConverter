# import collections
import os
import glob

import clique


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

        self.selected_collections = []
        for dir_collection in dir_collections:
            for collection in collections:
                if collection.head.replace("\\","/") == dir_collection.head.replace("\\","/"):
                    self.add_properties(dir_collection)
                    self.selected_collections.append(dir_collection)
            for remainder_item in remainder:
                if remainder_item.startswith(dir_collection.head.replace("\\","/")):
                    self.add_properties(dir_collection)
                    self.selected_collections.append(dir_collection)
                    
    def add_properties(self, collection):
        collection.start = str(collection).split()[1].replace('[','').replace(']','').split('-')[0]
        collection.end = str(collection).split()[1].replace('[','').replace(']','').split('-')[1]

        shortname = os.path.basename(collection.head)
        folder =  os.path.dirname(collection.head)
        if shortname[-1] in ['.', '_']:
            shortname = shortname[:-1]
        collection.shortname = shortname
        collection.folder = folder
    
    @property
    def sequences(self):
        return self.selected_collections

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