'''
Created on 2013骞�鏈�鏃�

@author: agz
'''
# Filename:backup_ver1.py
import os
import time

# must install the WinRAR tool
def winRar():
    # 1.The files and directories to be backed up are specified in alist.
    source = r'D:\GitHub\GitPython\books'
    # 2.The backup must be stored in a main backup directory
    target_dir = 'D:\\'
    # 3.The files are backed up into a rar file.
    # 4.The name of the rar archive is the current date and time
    target = target_dir + time.strftime('%Y%m%d%H%M%S') + '.rar'
    # 5.We use the rar command to put the files in a zip archive
    rar_command = 'rar a {0} {1}'.format(target, source)
    # Run the backup_ver1
    if os.system(rar_command) == 0:
        print("Successful backup to", target)
    else:
        print("Backup FAILED")

if __name__ == '__main__':
    pass
