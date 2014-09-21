'''
Created on 2013年9月19日

@author: Administrator
'''
import tarfile
from contextlib import closing


line = "你好"
# print(os.listdir('.'))
with closing(tarfile.open(r'..\lan.tgz', mode = 'w:gz')) as out:
#     for fn in os.listdir('.'):
#     out.add('.')
    info = out.gettarinfo(r'Zfile.py', arcname = 'Zfile.pysss')
    out.addfile(info)
if __name__ == '__main__':



    pass
