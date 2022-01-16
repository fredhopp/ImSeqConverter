import os
import subprocess
import asyncio
from ffmpeg import FFmpeg

from constants import FFMPEG_PATH

class ConvertToMovie:
    def __init__(self, sourcepath='', outputfolder='', filename='', format='mp4',framerate=23.976,startframe=1001): 
        self.framerate = framerate
        self.sourcepath = os.path.normpath(sourcepath)
        self.outputfolder = outputfolder
        self.filename = filename
        self.startframe = startframe
        self.format = format
        self.destinationfile = os.path.join(os.path.normpath(self.outputfolder), f'{self.filename}.{self.format}')
        self.to_mp4()
    
    def to_mp4(self):
        destinationfile = os.path.join(self.outputfolder, '{self.filename}.{self.format}')
        ffmpegpath = os.path.normpath(FFMPEG_PATH)
        command =  f'{ffmpegpath} -framerate {self.framerate} -start_number {self.startframe} -i {self.sourcepath} -c:v libx264 -crf 23 -pix_fmt yuv420p -y {self.destinationfile}'
        # -y -> overwrite outputfile
        # output = subprocess.run(command, capture_output=True)
        print(command)
        


ffmpeg = FFmpeg(executable='C:/Users/fredhopp/Downloads/ffmpeg-2022-01-03-git-68d0a7e446-full_build/bin/ffmpeg.exe').option('y').input(
    r'Z:\jobs\RD_210926\Data\research\mp4Converter\apps\fusion\renders\hyq010_All_bty\v018\dev010_lin_l1.%04d.jpg',
    start_number=1001,
).output(
    r'C:\Users\fredhopp\Desktop\test.mp4',
    # Use a dictionary when an option name contains special characters
    
    {'c:v': 'libx264'},
    crf='23',
    pix_fmt='yuv420p',
)

# @ffmpeg.on('start')
# def on_start(arguments):
#     print('Arguments:', arguments)

# @ffmpeg.on('stderr')
# def on_stderr(line):
#     print('stderr:', line)

@ffmpeg.on('progress')
def on_progress(progress):
    print(progress)

# @ffmpeg.on('progress')
# def time_to_terminate(progress):
#     # Gracefully terminate when more than 200 frames are processed
#     if progress.frame > 200:
#         ffmpeg.terminate()

@ffmpeg.on('completed')
def on_completed():
    print('Completed')

# @ffmpeg.on('terminated')
# def on_terminated():
#     print('Terminated')

# @ffmpeg.on('error')
# def on_error(code):
#     print('Error:', code)

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
    