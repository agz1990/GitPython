'''
Created on 2013年9月19日

@author: Administrator
'''
import os
import tarfile
from contextlib import closing

print(os.listdir('.'))
with closing(tarfile.open(r'..\lan.tgz', mode = 'w:gz')) as out:
#     for fn in os.listdir('.'):
    out.add('.')

if __name__ == '__main__':



    pass
