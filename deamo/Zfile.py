'''
Created on 2013年9月6日

@author: agz
'''
# coding: utf-8
# xxteach.com
import zipfile
import os.path


class ZFile(object):
    def __init__(self, filename, mode = 'r', basedir = ''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression = zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)

    def addfile(self, path, arcname = None):
        path = path.replace('//', '/')
        if not arcname:
            if path.startswith(self.basedir):
                arcname = path[len(self.basedir):]
            else:
                arcname = ''
        self.zfile.write(path, arcname)

    def addfiles(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)

    def close(self):
        self.zfile.close()

    def extract_to(self, path):
        for p in self.zfile.namelist():
            self.extract(p, path)

    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dirName = os.path.dirname(f)
            if not os.path.exists(dirName):
                os.makedirs(dirName)
            open(f, 'wb').write(self.zfile.read(filename))


def create(zfile, files):
    z = ZFile(zfile, 'w')
    z.addfiles(files)
    z.close()

def extract(zfile, path):
    z = ZFile(zfile)
    z.extract_to(path)
    z.close()

#
def zipFile(zfile, path = '.', rules = ''):
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fName = os.path.join(dirpath, filename)
            print(fName)
            files.append(fName)
    f = zipfile.ZipFile(zfile, 'w', zipfile.ZIP_DEFLATED)
    for fname in files:
        f.write(fname)
    f.close()


def uZipFile(zfile, path = '.'):
    extract(zfile, path)


if __name__ == '__main__':
    zipFile('zipFile.zip', r'..')
#     uZipFile('text.zip', r'..')
    print('done...')

