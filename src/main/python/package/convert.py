import os
import subprocess

from constants import FFMPEG_PATH

class ConvertToMovie:
    def __init__(self, sourcepath, destinationfile=''): 
        self.to_mp4(sourcepath=sourcepath, destinationfile=destinationfile)
    
    def to_mp4(self, framerate=23.976, sourcepath='', destinationfile=''):
        command =  f'{FFMPEG_PATH} -framerate {framerate} -i {sourcepath} -c:v libx264 -crf 23 -pix_fmt yuv420p {destinationfile}.mp4'
        # ffmpeg -framerate 30 -i DSC_%04d.JPG -c:v libx264 -crf 23 -pix_fmt yuv420p output.mp4
        output = subprocess.run(command, capture_output=True)
        print(output.stdout)
        


if __name__=='__main__':
    i = ConvertToMovie('Z:/jobs/RD_210926/Data/research/mp4Converter/apps/fusion/renders/hyq010_All_bty/v018/dev010_lin_l1.%04d.jpg','C:/Users/fredhopp/Desktop/test')
    