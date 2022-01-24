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
        self.format = format
        self.framerange = framerange
        self.destinationfile = os.path.join(os.path.normpath(self.outputfolder), f'{self.filename}.{self.format}')
    
    def to_movie(self):
        ffmpegpath = FFMPEG_PATH.replace('\\','/')
        sourcepath = self.sourcepath.replace('\\','/')
        destinationfile = self.destinationfile.replace('\\','/') # testing on a windows 10 OS

        # ffmpeg_args = f'-start_number {self.startframe} -i "{sourcepath}" -vframes {self.framerange} -c:v libx264 -vf format=yuv420p "{destinationfile}"'
        ffmpeg_args = f'-start_number {self.startframe} -y -i "{sourcepath}" -vframes {self.framerange} -c:v libx264 -vf format=yuv420p "{destinationfile}"'

        ffmpeg_command = f'"{ffmpegpath}" {ffmpeg_args}'.replace('/','\\')
        returned_value = subprocess.call(ffmpeg_command, shell=True)
        print(returned_value)
        if not returned_value:
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
    