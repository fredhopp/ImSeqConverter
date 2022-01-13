import os



# cannot inherit class Image 
class ConvertToMovie:
    def __init__(self, path, folder='resized'): 
        #  path needs to be fwd slash
        # self.image = Image.open(path)
        # self.width, self.height = self.image.size
        # self.path = path
        # self.resize_path = os.path.join(os.path.dirname(self.path), 
        #                                 folder,
        #                                 os.path.basename(self.path)).replace('\\', '/')
        pass
    
    def to_mp4(self, size=.5, quality=75):
        # new_width = round(self.width * size)
        # new_height = round(self.height * size)
        # self.image = self.image.resize((new_width, new_height), Image.ANTIALIAS)

        # parent_dir = os.path.dirname(self.resize_path)
        # if not os.path.exists(parent_dir):
        #     os.makedirs(parent_dir)
            
        # self.image.save(self.resize_path, 'JPEG', quality=quality)
        # return os.path.exists(self.resize_path)
        pass


if __name__=='__main__':
    i = ConvertToMovie('Z:/Programming/PyConverter/src/main/resources/images/pinup.jpg')
    