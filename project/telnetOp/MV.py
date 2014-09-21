#!/usr/bin/python3
# encoding=utf-8
from string import Template
from telnetlib import Telnet
import os
import string
import sys
TftpHost = '192.168.1.133'
MachineIp = '192.168.1.234'
User = 'root'
Password = 'solokey'

PC_MTD_DIR = r'/mnt/hgfs/work_folder/main_code/firmware3.0/trunk/'
MACHINE_MTD_DIR = r'/mnt/mtdblock/'

Commands = ['cd /mnt/mtdblock', 'echo "Hello Machine." > TelnetShell', './app/sms/sms >/dev/null&']

MV_MSG = Template("""\033[0;32m
################################################################################
# TftpHost  :\t\033[4;33m${tftpHost}\033[0;32m
# Machine   :\t\033[4;33m${machineIP}\033[0;32m
# BIN       :\t${bin}
# PATH      :\t${path}
################################################################################
\033[0m""")

class TelnetShell(Telnet):
    def __init__(self, tftpHost=TftpHost, host=MachineIp, user=User,
                 password=Password, timeout=5, port=23):
        self.cmdFinish = '#'
        self.status = ['done', 'error', 'success']
        self.runlog = []
        self.smsg = "TelnetShell|^#"
        self.encode = 'ascii'
        self.MachineIP = host
        self.ServiceIP = tftpHost
        self.input = '\033[0;31m' + self.MachineIP + "@ZMM100# " + '\033[0;32m'
        super(TelnetShell, self).__init__(host, port, timeout)
        self.connect(host, user, password)



    def writeString(self, _str, encode):
        buffer = _str.encode(encode)
        self.write(buffer)
        pass

    def egrepPrint(self, _str, filter=None, dest=None):

        tripset = string.whitespace + '#'
        if len(_str.strip(tripset)) == 0:
            return
        _str = self.input + _str.strip(tripset)
        print(_str, end='')

    def mv(self, r, l):
        ip = self.ServiceIP
        r = os.path.basename(r)
        cmd = 'tftp -g %s -r %s && chmod 755 %s && mv %s %s ' % (ip, r, r, r, l)
        self.sh(cmd)


    def unzip(self, tarfile, dest):
        self.mv(tarfile, tarfile)
        defaultTimeout = self.timeout
        self.timeout = 120
        ret = self.sh('tar', '-zxvf', tarfile, '-C', dest)
        self.timeout = defaultTimeout
        self.sh('rm', tarfile, '-rf &')
        return ret


    def connect(self, Host, username, password, timeout=10):
        # 输入登录用户名
        self.readString_until('login:')
        cmd = username + '\n'
        self.writeString(cmd, self.encode)
        # 输入登录密码
        self.readString_until('Password:')
        cmd = password + '\n'
        self.writeString(cmd, self.encode)
        # 登录完毕后执行命令
        self.readString_until('#')


    def readString_until(self, _str, timeout=10):
        match = _str.encode(self.encode)
        retBuffer = self.read_until(match, timeout)
        return retBuffer.decode(self.encode)

    def sh(self, _str, argv=''):
        print(argv)
        args = ' '.join(argv)
        _str = _str + ' ' + args + '\n'
        self.writeString(_str, self.encode)
        return self.waitForCmdFinish(self.timeout)

    def runCmds(self, cmds):
        ret = []
        for cmd in cmds:
            ret.append(self.sh(cmd))

    def waitForCmdFinish(self, timeout=120):
#         print("wait...")
        while True:
            mach = '#'   # % (self.cmdFinish, timeout)
            et = self.encode
            ret = self.readString_until(mach, timeout)
            self.egrepPrint(ret)
            if ret[-1] == self.cmdFinish:
                self.writeString("echo $?\n", et)
                ret = self.readString_until(mach, 1)
                return bool(ret[-4])

    def execShellBash(self, file, *argv):
        print(argv)
        newfile = '/root/' + file
#         print(newfile)
        if  self.mv(file, newfile) == 0:
            self.sh(newfile, argv)
            self.sh('rm', newfile, '-rf')


if __name__ == '__main__':
    if len(sys.argv) == 5:
        
        detail = {}
        detail['tftpHost'] = sys.argv[1]
        detail['machineIP'] = sys.argv[2]
        destFile = sys.argv[4]
        detail['path'] = os.path.dirname(destFile)
        detail['bin'] = os.path.basename(destFile)
        msg = MV_MSG.safe_substitute(detail)
        print(msg)
        try:
            ts = TelnetShell(sys.argv[1], sys.argv[2])
        except OSError as e:
            print(e)
            exit(0)
        ts.mv(sys.argv[3], sys.argv[4])
        ts.sh('date')
        ts.close()   # tn.write('exit\n')
        print("\n\n")
    exit(0)


