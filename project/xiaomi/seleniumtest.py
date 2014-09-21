#!/usr/bin/python
# -*- coding: utf-8 -*-
from MyWeb import MiWeb
from ctypes.test.test_errno import threading
from selenium import webdriver
import User
from selenium.webdriver.common.proxy import *
myProxy = "127.0.0.1:8087"

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': ''  # set this value as desired
    })


LCDW = 1920
LCDH = 1000

TestUser = User.WebUser()
Userinfodb = "u.txt"
# OrderURL = 'file:///' + os.path.abspath('yuyue.html')

def readUserInfofromFile(fname):
    userinfos = []
    with open(fname, 'r') as f:
        for eachline in f:
            ret = eachline.split()
            if len(ret) == 2 :
                userinfos.append(ret)
    return userinfos

def procMiOrder(user, browser):

    miweb = MiWeb(user, browser)
    miweb.order()

def mainloop():
    ts = []
    userinfos = readUserInfofromFile(Userinfodb)
    for iCnt, oneuser in enumerate(userinfos):
        user = User.WebUser()
        profile = webdriver.FirefoxProfile(r"C:\Program Files\Mozilla Firefox\firefox.exe")
        profile.set_preference("general.useragent.override", "Mozilla/4.0 (compatible: MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; SAMSUNG; SGH-i917)")
        browser = webdriver.Firefox(firefox_profile=profile)
#         x = (iCnt % 4) * LCDW / (len(userinfos) / 2)
#         y = (iCnt / 4) * (LCDH / 2)
#         browser.set_window_position(x, y)
#         browser.set_window_size(LCDW / (len(userinfos) / 2) , LCDH / 2)

        t = threading.Thread(target=procMiOrder, args=(user, browser))
        t.start()
        ts.append(t)

    for t in ts:
        t.join()
    pass

mainloop()

