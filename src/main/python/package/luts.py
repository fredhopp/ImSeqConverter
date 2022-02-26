import os
import glob

import package.preferences as preferences
# import preferences # local exec

colorspace_name_separator = '_'

class Luts:
    def __init__(self):
        self.lut_dir = preferences.browse_load('lut_dir')
        self.colorspace_name_separator = '_'
    
    @property
    def lut_files(self):
        glob_search_str = os.path.join(self.lut_dir,'*.csp')
        if lut_files := glob.glob(glob_search_str):
            lut_files = [file.replace('\\','/') for file in lut_files]
            return lut_files
        else:
            return
               
    def get_luts(self):
        '''
        Returns a dictionnary of luts with.
        key: Source Lut
        value: List of Target Luts
        '''
        if not (lut_files := self.lut_files):
            return
        file_names = [os.path.basename(lut_file) for lut_file in lut_files]
        colorspace_sources = [file_name.split( self.colorspace_name_separator)[0] for file_name in file_names]
        colorspace_sources = set(list(colorspace_sources)) # uniquify
        lut_pairs = {} # init dict
        for colorspace_source in colorspace_sources:
            colorspace_targets = []
            for file_name in file_names :
                file_prefix = file_name.split( self.colorspace_name_separator)[0]
                if colorspace_source == file_prefix:
                    colorspace_target = '.'.join(file_name.split(self.colorspace_name_separator)[-1].split('.')[:-1])
                    colorspace_targets.append(colorspace_target)
            lut_pairs[colorspace_source] = colorspace_targets
        lut_pairs['--Ignore--'] = ['--Ignore--']
        
        return lut_pairs
        
        
if __name__ == '__main__':
    luts = Luts()
    print(luts.luts)
