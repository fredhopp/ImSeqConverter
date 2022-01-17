import os
# import subprocess
import asyncio
from ffmpeg import FFmpeg

from constants import FFMPEG_PATH

class ConvertToMovie:
    def __init__(self, sourcepath='', outputfolder='', filename='', format='mp4', framerate=23.976, startframe=1001): 
        self.framerate = framerate
        self.sourcepath = sourcepath.replace('/','\\')
        self.outputfolder = outputfolder
        self.filename = filename
        self.startframe = startframe
        self.format = format
        self.destinationfile = os.path.join(os.path.normpath(self.outputfolder), f'{self.filename}.{self.format}')
        self.to_mp4()
    
    def to_mp4(self):
        destinationfile = os.path.join(self.outputfolder, f'{self.filename}.{self.format}')
        destinationfile = destinationfile.replace('/','\\')
        ffmpegpath = FFMPEG_PATH.replace('\\','/')
        # command =  f'{ffmpegpath} -framerate {self.framerate} -start_number {self.startframe} -i {self.sourcepath} -c:v libx264 -crf 23 -pix_fmt yuv420p -y {self.destinationfile}'
        # -y -> overwrite outputfile
        # output = subprocess.run(command, capture_output=True)
        # print(destinationfile)
        


        ffmpeg = FFmpeg(executable=FFMPEG_PATH).option('y').input(
            self.sourcepath,
            start_number=self.startframe,
        ).output(
            destinationfile,
            # Use a dictionary when an option name contains special characters
            {'c:v': 'libx264'},
            crf='23',
            pix_fmt='yuv420p',
        )

        @ffmpeg.on('progress')
        def on_progress(progress):
            print(progress)

        @ffmpeg.on('completed')
        def on_completed():
            print('Completed')


        loop = asyncio.get_event_loop()
        loop.run_until_complete(ffmpeg.execute())
        loop.close()

if __name__=='__main__':
    i = ConvertToMovie(sourcepath='Z:/jobs/airforce_210419/Data/own/own470/publish/images/plates/own470_l1_lin/v001/own470_l1_lin_v001.%04d.exr',
                        outputfolder='C:/Users/fredhopp/Desktop',
                        filename='test',
                        format='mp4',
                        framerate=10,
                        startframe=1001)
    