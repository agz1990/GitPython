'''
Created on 2013年9月5日

@author: hp41
'''
# 工程配置文件  rule.py
import ntpath
import os

#工程路径
alsep=' \ '.strip() #路径分隔符
lnsep=os.linesep    #换行符


WOKR_DIR= os.path.abspath('.')  #工作路径
TEMP_DIR= WOKR_DIR + alsep + 'tmp'  #临时文件路径
RES_DIR=WOKR_DIR + alsep + 'res'    #资源文件路径
DATA_DIR=WOKR_DIR + alsep + 'data'  #数据文件路径


DIRS=[WOKR_DIR,TEMP_DIR,RES_DIR,DATA_DIR]
def pathCheck(name,value):
    print("%-10s: %-50s  [%s]"%(name,value,os.path.isdir(value)))
   

        
def Details():
    print('Woke Rule Value:')
    pathCheck('WOKR_DIR',WOKR_DIR);
    pathCheck('TEMP_DIR',TEMP_DIR);
    pathCheck('RES_DIR',RES_DIR);
    pathCheck('DATA_DIR',DATA_DIR);
if __name__ == '__main__':
    Details()
