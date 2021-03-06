import os
import subprocess
# import asyncio
# from ffmpeg import FFmpeg

from package.constants import FFMPEG_PATH, LUT_PATH, FONT
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
                colorspaceIn='None',
                colorspaceOut='None',
                overlay_framenum=False,
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
        self.colorspaceIn = colorspaceIn
        self.colorspaceOut = colorspaceOut
        self.overlay_framenum = overlay_framenum 
        self.destinationfile = os.path.join(os.path.normpath(self.outputfolder), f'{self.filename}.{self.extension}')
    
    def to_movie(self):
        ffmpegpath = FFMPEG_PATH.replace('/','\\')
        sourcepath = self.sourcepath.replace('/','\\')
        destinationfile = self.destinationfile.replace('/','\\') # testing on a windows 10 OS

        use_lut = self.colorspaceIn != self.colorspaceOut
        lut_name = f'{self.colorspaceIn}_{self.colorspaceOut}.csp'
        lut_path = os.path.join(LUT_PATH,lut_name)
        lut_path = self.ffmpegFilter_path(lut_path)
        ffmpeg_lut_arg = ''
        if use_lut:
            ffmpeg_lut_arg = f'lut3d={lut_path},' # include comma, so that we can skip the overlay altogether in the command if needed

        font_path = FONT
        font_path = self.ffmpegFilter_path(font_path)
        ffmpeg_frameOverlay_arg = ''
        if self.overlay_framenum:
            ffmpeg_frameOverlay_arg = (f'drawtext=fontfile={font_path}:'
                                        r"text='%{frame_num}':"
                                        f'start_number={self.startframe}:'
                                        r'x=(w-tw)/2:'
                                        # r"y=h-(2*lh):" # jitters because ofvariable character height :(
                                        r'y=h-ceil(h/20):'
                                        r'fontcolor=LightGrey:'
                                        r'fontsize=ceil(h/20):'
                                        r'box=0:'
                                        r'alpha=.5'
                                        r',' # include comma, so that we can skip the overlay altogether in the command if needed
                                        )

        # adding black pixel padding for uneven resolutions -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"
        if self.extension == 'mp4':
            dic_quality = {'High': 18, 'Medium': 23, 'Low': 28} # -crf 0-51 0:lossless 23:default 51:worst -> usually between 18-28
            # adding black pixel padding for uneven resolutions
            ffmpeg_args = f'-start_number {self.startframe} -y -framerate {self.fps} -i "{sourcepath}" -vframes {self.framerange} -c:v libx264 -crf {dic_quality[self.quality]} -vf "{ffmpeg_frameOverlay_arg}{ffmpeg_lut_arg}format=yuv420p,pad=ceil(iw/2)*2:ceil(ih/2)*2" "{destinationfile}"'
        
        else:  # prores
            dic_quality = {'High': 2, 'Medium': 1, 'Low': 0} # -profile:v -> proxy (0) lt (1) standard (2) hq (3)
            ffmpeg_args = f'-start_number {self.startframe} -y -framerate {self.fps} -i "{sourcepath}"  -vframes {self.framerange} -c:v prores_ks -profile:v {dic_quality[self.quality]} -vendor apl0 -pix_fmt yuv422p10le -vf "{ffmpeg_frameOverlay_arg}{ffmpeg_lut_arg}pad=ceil(iw/2)*2:ceil(ih/2)*2" "{destinationfile}"'
                

        ffmpeg_command = f'"{ffmpegpath}" {ffmpeg_args}' #.replace('/', '\\')
        print(ffmpeg_command)
        returned_value = subprocess.call(ffmpeg_command, shell=False)

        if not returned_value:  # exit code 0 means successful
            return True

    # for filters, ffmpeg needs something like "Z\:/path/to/the/lut.csp" on Windows 10
    def ffmpegFilter_path(self, path):
        path_list = path.split(':')
        path_list[0] = f'{path_list[0]}\\\\'
        path_list[1] = path_list[1].replace('\\','/')
        path = ':'.join(path_list)
        return path
        

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
    