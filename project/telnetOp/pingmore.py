import os
import re
import time
import sys
from threading import Thread

aliveInfo = re.compile(r"TTL=")
status = ("No response", "Partial Response", "Alive")


class IpAddr(Thread):
    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = 0

    def run(self):
        pingaling = os.popen("ping -n 1 " + self.ip, "r")

        while 1:
            line = pingaling.readline()
            if not line:
                break;
#             print(line)
            igot = re.findall(aliveInfo, line)
            if igot:
                self.status = 2


class LifeIp() :
    def __init__(self) :
        self.pingList = []
        try :
            ip_conf_file = open("ip_conf.txt", 'r')
        except :
            self.startIp = '192.168.1.132'
            self.endIp = '192.168.1.254'
        else :
            for line in ip_conf_file :
                conf_item = line.replace('\n', '').split('=')
                if 'start_ip' in conf_item :
                    self.startIp = conf_item[1]
                else :
                    self.endIp = conf_item[1]

    def getStatus(self) :
        start_ip_items = self.startIp.split('.')
        end_ip_items = self.endIp.split('.')
        print(start_ip_items)
        for first in range(int(start_ip_items[0]), int(end_ip_items[0]) + 1) :
            for second in range(int(start_ip_items[1]), int(end_ip_items[1]) + 1) :
                for third in range(int(start_ip_items[2]), int(end_ip_items[2]) + 1) :
                    for four in range(int(start_ip_items[3]), int(end_ip_items[3]) + 1) :
                        ip = str(first) + '.' + str(second) + '.' + str(third) + '.' + str(four)
                        pingIp = IpAddr(ip)
                        self.pingList.append(pingIp)
                        pingIp.start()

    def showStatus(self) :
        for pingIp in self.pingList :
            pingIp.join()
            print (pingIp.ip + ' : ' + status[pingIp.status])


if __name__ == '__main__':
    print (time.ctime())
    ci = LifeIp()
    ci.getStatus()
    ci.showStatus()
