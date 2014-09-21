#!/usr/bin/python
# -*- coding: utf-8 -*-

class WebUser(object):
    '''
    用户信息
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.uid = '13423997110'
        self.pwd = 'qq0507108063'
        self.name = '纪国铖'
        self.email = '522360568@qq.com'
        self.tel = '13423997110'
        self.province = '广东'
        self.city = '深圳市'
        self.district = '龙岗区'
        self.addr = '五和大道华为总部'
        self.postalcode = '515000'
        self.userinfos = []

class WebUsers():
    def __init__(self, fname):
        self.users = []
        self.readUserInfofromFile(fname)


    def readUserInfofromFile(self, fname):
        with open(fname, 'br') as f:
            for eachline in f:
                ret = eachline.decode().split()
                if len(ret) == 10 :
                    user = WebUser()
                    user.uid = ret[0]
                    user.pwd = ret[1]
                    user.name = ret[2]
                    user.email = ret[3]
                    user.tel = ret[4]
                    user.province = ret[5]
                    user.city = ret[6]
                    user.district = ret[7]
                    user.addr = ret[8]
                    user.postalcode = ret[9]
                    self.users.append(user)
                    print(ret)
            self.users.reverse()

    def getNextUser(self):
        if len(self.users) :
            user = self.users.pop()
            print(user.uid, user.name)
            return user
        else:
            return None
