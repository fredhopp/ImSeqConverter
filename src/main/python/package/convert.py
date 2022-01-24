import os
import subprocess
# import asyncio
# from ffmpeg import FFmpeg

from package.constants import FFMPEG_PATH
# from constants import FFMPEG_PATH # use for __main__ execution

class ConvertToMovie():
    def __init__(self, 
                sourcepath='',
                filename='',
                format='mp4',
                quality='High',
                fps='23.976',
                startframe=1001,
                framerange=2,
                outputfolder=''
                ):
        self.fps = float(fps)
        self.sourcepath = sourcepath
        self.outputfolder = outputfolder
        self.filename = filename
        self.startframe = startframe
        if format=='prores-mov':
            format='mov'
        self.extension = format
        self.quality = quality
        self.framerange = framerange
        self.destinationfile = os.path.join(os.path.normpath(self.outputfolder), f'{self.filename}.{self.extension}')
    
    def to_movie(self):
        ffmpegpath = FFMPEG_PATH.replace('\\','/')
        sourcepath = self.sourcepath.replace('\\','/')
        destinationfile = self.destinationfile.replace('\\','/') # testing on a windows 10 OS

        if self.extension == 'mp4':
            dic_quality = {'High': 18, 'Medium': 23, 'Low': 28}
            # -crf 0-51 0:lossless 23:default 51:worst -> usually between 18-28
            ffmpeg_args = f'-start_number {self.startframe} -y -i "{sourcepath}" -vframes {self.framerange} -c:v libx264 -crf {dic_quality[self.quality]} -vf format=yuv420p "{destinationfile}"'
        else:  # prores
            dic_quality = {'High': 3, 'Medium': 2, 'Low': 1}
            # -profile:v -> lt (1) standard (2) hq (3)
            ffmpeg_args = f'-start_number {self.startframe} -y -i "{sourcepath}" -vframes {self.framerange} -c:v prores_ks -profile:v {dic_quality[self.quality]} -vendor apl0 -pix_fmt yuv422p10le "{destinationfile}"'

        ffmpeg_command = f'"{ffmpegpath}" {ffmpeg_args}'.replace('/', '\\')
        returned_value = subprocess.call(ffmpeg_command, shell=False)
        
        if not returned_value:  # exit code 0 means successful
            return True
        

if __name__=='__main__':
    i = ConvertToMovie(sourcepath='Z:/jobs/airforce_210419/Data/own/own470/publish/images/plates/own470_l1_lin/v001/own470_l1_lin_v001.%04d.exr',
                        filename='test',
                        format='mp4',
                        fps=23.976,
                        startframe = 1001,
                        framerange = 20,
                        outputfolder = 'C:/Users/fredhopp/Desktop/',
                        )
    i.to_movie()
    