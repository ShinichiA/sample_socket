import os
import time


class Scan:
    def __init__(self, folder):
        self.folder = folder
        self.last_image = None
        self.last_image_time = None
        os.chdir(self.folder)

    def get_last_image(self, retry=0):
        files = filter(os.path.isfile, os.listdir(self.folder))
        files = [os.path.join(self.folder, f) for f in files]  # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))

        for file in files:
            if file.endswith(".jpg"):
                print(file)
                path = os.path.join(self.folder, file)
                while retry < 10:
                    old_size = os.path.getsize(path)
                    time.sleep(0.1)
                    new_size = os.path.getsize(path)
                    if old_size != new_size:
                        retry += 1
                        continue
                    stat = os.stat(path)
                    self.last_image_time = stat.st_ctime
                    return path
        return None
