import os
import subprocess
import json
import sys
import time
import gc
import math
# import logging

from PySide6 import QtWidgets
import package.preferences as preferences

class ConvertToMovie():
    def __init__(self, 
                sourcepath='',
                filename='',
                format='mp4-h.264',
                quality='High',
                fps='23.976',
                startframe=1001,
                framerange=2,
                colorspaceIn='None',
                colorspaceOut='None',
                overlay_framenum=False,
                overlay_title=False,
                resolution='Original',
                outputfolder='',
                seqtype='IMG',
                dialog=QtWidgets.QProgressDialog,
                ):
        # self.sub_logger = logging.getLogger('__main__')
        pref_dir = preferences.default_path()
        pref_file = os.path.join(pref_dir,'preferences.json')
        self.dialog = dialog
        if os.path.exists(pref_file):
            with open(pref_file, 'r') as pref_file:
                json_object = json.load(pref_file)
                for key, value in json_object.items():
                    if key == 'ffmpeg_dir':
                        self.FFMPEG_PATH = os.path.join(value,'ffmpeg.exe')
                    elif key == 'font_file':
                        self.FONT_PATH = value
                    elif key == 'lut_dir':
                        self.LUT_PATH = value

        self.fps = float(fps)
        self.sourcepath = sourcepath
        self.outputfolder = outputfolder
        self.filename = filename
        self.startframe = startframe
        self.extension = 'mp4'
        self.format = format
        if format=='mov - prores':
            self.extension = 'mov'
        self.quality = quality
        self.framerange = framerange
        self.colorspaceIn = colorspaceIn
        self.colorspaceOut = colorspaceOut
        self.overlay_framenum = overlay_framenum
        self.overlay_title = overlay_title
        self.resolution = resolution
        self.destinationfile = os.path.join(os.path.normpath(self.outputfolder), f'{self.filename}.{self.extension}')
        self.seqtype = seqtype

    
    def to_movie(self):   # sourcery skip: assign-if-exp, introduce-default-else
        ffmpegpath = self.FFMPEG_PATH.replace('/','\\')
        sourcepath = self.sourcepath.replace('/','\\')
        destinationfile = self.destinationfile.replace('/','\\') # testing on a windows 10 OS

        # ffmpeg LUT stuff
        use_lut = self.colorspaceIn != self.colorspaceOut
        lut_name = f'{self.colorspaceIn}_{self.colorspaceOut}.csp'
        lut_path = os.path.join(self.LUT_PATH,lut_name)
        lut_path = self.ffmpegFilter_path(lut_path)
        ffmpegArg_lut = ''
        if use_lut:
            ffmpegArg_lut = f'lut3d={lut_path},' # include comma, so that we can skip the lut if not needed

        # ffmpeg drawtext stuff
        font_path = self.FONT_PATH
        font_path = self.ffmpegFilter_path(font_path)
        ffmpegArg_frameOverlay = ''
        if self.overlay_framenum:
            ffmpegArg_frameOverlay = (f'drawtext=fontfile={font_path}:'
                                        r"text='%{frame_num}':"
                                        f'start_number={self.startframe}:'
                                        r'x=(w-tw)/2:'
                                        # r"y=h-(2*lh):" # jitters because of variable character height :(
                                        r'y=h-ceil(h/20):'
                                        r'fontcolor=LightGrey:'
                                        r'fontsize=ceil(h/20):'
                                        r'box=0:'
                                        r'alpha=.5'
                                        r',' # include comma, so that we can skip the overlay altogether in the command if not needed
                                        )
        ffmpegArg_titleOverlay = ''
        if self.overlay_framenum:
            ffmpegArg_titleOverlay = (f'drawtext=fontfile={font_path}:'
                                        f'text={self.filename}:'
                                        r'x=(w-tw)/2:'
                                        r'y=5:' 
                                        r'fontcolor=LightGrey:'
                                        r'fontsize=ceil(h/20):'
                                        r'box=0:'
                                        r'alpha=.5'
                                        r',' # include comma, so that we can skip the overlay altogether in the command if not needed
                                        )

        # ffmpeg resizing related stuff
        dic_res = {'1080p':(1920,1080),'UHD':(3840,2160)}
        if self.resolution != 'Original':
            hres = dic_res[self.resolution][0]
            vres = dic_res[self.resolution][1]
            ffmpeg_scale_arg = f'scale=(iw*sar)*min({hres}/(iw*sar)\\,{vres}/ih):ih*min({hres}/(iw*sar)\\,{vres}/ih),' # include comma, so that we can skip in the command if not needed
            ffmpeg_pad_arg = f'pad={hres}:{vres}:({hres}-iw*min({hres}/iw\\,{vres}/ih))/2:({vres}-ih*min({hres}/iw\\,{vres}/ih))/2' # not including',' since it's the last arg of the -vf section
        else:
            ffmpeg_scale_arg = ''
            ffmpeg_pad_arg = 'pad=ceil(iw/2)*2:ceil(ih/2)*2' # adding black pixel padding for uneven resolutions -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"


        # ffmpeg compression related stuff
        if self.format in ['mp4 - h.264', 'mp4 - h.265']:    
            h26x_lib_version = self.format[-1]
            dic_quality = {'High': 13, 'Medium': 23, 'Low': 28} # -crf 0-51 0:lossless 23:default 51:worst -> usually between 18-28 (old values: 18,23,28)
            ffmpegArg_compression1 = f'-c:v libx26{h26x_lib_version} -crf {dic_quality[self.quality]}'
            ffmpegArg_compression2 = 'format=yuv420p,' # include comma, so that we can skip in the command if not needed
        elif self.format == 'mov - prores':
            dic_quality = {'High': 2, 'Medium': 1, 'Low': 0} # -profile:v -> proxy (0) lt (1) standard (2) hq (3)
            ffmpegArg_compression1 = f'-c:v prores_ks -profile:v {dic_quality[self.quality]} -vendor apl0 -pix_fmt yuv422p10le'
            ffmpegArg_compression2 = '' # skipped in prores_ks, to be verified

        ffmpeg_args = f'-start_number {self.startframe} -y -framerate {self.fps} -i "{sourcepath}" -vframes {self.framerange} {ffmpegArg_compression1} -vf "{ffmpegArg_frameOverlay}{ffmpegArg_titleOverlay}{ffmpegArg_lut}{ffmpegArg_compression2}{ffmpeg_scale_arg}{ffmpeg_pad_arg}" "{destinationfile}"'
        if self.seqtype == 'MOV':
            start_timecode = self.startframe/self.fps
            end_timecode = self.framerange/self.fps            
            ffmpegArg_timecode = f'-ss {start_timecode} -t {end_timecode} -async 1 -strict -2'            
            ffmpeg_args = f'-y {ffmpegArg_timecode} -i "{sourcepath}" {ffmpegArg_compression1} -vf "{ffmpegArg_frameOverlay}{ffmpegArg_titleOverlay}{ffmpegArg_lut}{ffmpegArg_compression2}{ffmpeg_scale_arg}{ffmpeg_pad_arg}" "{destinationfile}"'

        file_progress_path = os.path.join(preferences.default_path(),'progress.buffer').replace('\\','/')
        ffmpeg_progress_args = f' -progress "{file_progress_path} "'
        ffmpeg_command = f'"{ffmpegpath}" {ffmpeg_progress_args} {ffmpeg_args}'
        # returned_value = subprocess.call(ffmpeg_command, shell=False)
        
        # self.sub_logger.info(f'ffmpeg command: {ffmpeg_command}')
        
        if not os.path.exists(file_progress_path):
            file = open(file_progress_path, 'w')
            file.close()
        file_progress = open(file_progress_path, 'r', encoding = 'utf-8')
        process = subprocess.Popen(ffmpeg_command,
                                   shell = False,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                    universal_newlines=False,
                                    )
        while True:
            shell_line = process.stdout.readline()
            if shell_line:
                # Print FFmpeg output to console for debugging
                try:
                    output_line = shell_line.decode('utf-8', errors='ignore').strip()
                    if output_line and not output_line.startswith('frame='):
                        print(f"[FFmpeg] {output_line}")
                except:
                    pass
            
            where = file_progress.tell()
            if line := file_progress.readline():
                if line.startswith('frame='):
                    percentage = math.ceil(float(line.split("=")[-1])/float(self.framerange)*100.0)
                    text = f'{self.filename} \nEncoding: {percentage} %' # frame: {line.split("=")[-1]}'
                    self.dialog.label.setText(text)
                    print(f"[Progress] {self.filename}: {percentage}%")
            else:
                # time.sleep(.5)
                file_progress.seek(where)
            # sys.stdout.flush()
            if not shell_line:
                break


        returned_value = process.returncode
        if not returned_value:  # exit code 0 means successful
            return True

    # for filters, ffmpeg needs something like "Z\:/path/to/the/lut.csp" on Windows 10
    def ffmpegFilter_path(self, path):
        path_list = path.split(':')
        path_list[0] = f'{path_list[0]}\\\\'
        path_list[1] = path_list[1].replace('\\','/')
        path = ':'.join(path_list)
        return path
        

    