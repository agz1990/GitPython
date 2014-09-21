#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    ElementNotVisibleException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from time import sleep
import threading
import time


# 登录的网站
URLLogin = 'https://account.xiaomi.com/pass/serviceLogin'

# 预约的网站
URLOrder = "http://a.hd.xiaomi.com/register/book/a/40"
IDUserName = 'username'
IDPwd = "userPwd"

Status = { "ready": [0, "准备就绪"],
          "logout":[0, "登出用户"],
           "login":[10, "登录网页"],
          "preorder":[20, "进入预约界面"],
          "reorder":[20, "超时刷新预约界面"],
          "order":[40, "填写预约资料"],
         "inputCaptcha":[80, "等待输入验证码"],
         "success":[100, "预约成功"],
         "failed":[0, "预约失败"],
         "erraddr":[0, "地址输入有误！"],
          }


class MiThreadWeb():
    def __init__(self, setCurStatus, x=100, y=100, w=400, h=600):

        super(MiThreadWeb, self).__init__()
        self.user = None
        self.dr = None
        self.setCurStatus = setCurStatus

    def setUserInfo(self, user):
        self.user = user

    def getUserInfo(self):
        return self.user

    def setDriverRect(self, x, y, w, h):
        if self.dr == None:
#             profile = webdriver.FirefoxProfile()
#             profile.set_preference("general.useragent.override", "Mozilla/4.0 (compatible: MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; SAMSUNG; SGH-i917)")
#             self.dr = webdriver.Firefox(firefox_profile=profile)
            options = webdriver.ChromeOptions()
            options.add_argument('--user-agent=Mozilla/4.0 (compatible: MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; SAMSUNG; SGH-i917)')
            self.dr = webdriver.Chrome(chrome_options=options)
        self.dr.set_window_position(x, y)
        self.dr.set_window_size(w, h)

    def login(self):

        dr = self.dr
        user = self.user
        self.logout()
        self.setCurStatus(Status["ready"])
        try:
            dr.get(URLLogin)
            self.setCurStatus(Status["login"])
#             WebDriverWait(dr, 5).until(EC.frame_to_be_available_and_switch_to_it('miniLoginFrame'))
#             WebDriverWait(dr, 5).until(lambda dr: dr.find_element_by_id(u'miniLoginFrame').is_displayed())
#             dr.switch_to_frame("miniLoginFrame")

#             WebDriverWait(dr, 5).until(lambda dr: dr.find_element_by_id(u'miniLogin_username').is_displayed())
#             userid = dr.find_element_by_id('miniLogin_username')
#             userid.send_keys(user.uid)
#
#             pwdInput = dr.find_element_by_id ('miniLogin_pwd')
#             pwdInput.send_keys(user.pwd + Keys.RETURN)
#             WebDriverWait(dr, 5).until_not(lambda dr: dr.find_element_by_id('miniLogin_pwd').is_displayed())

            WebDriverWait(dr, 5).until(lambda dr: dr.find_element_by_id(IDUserName).is_displayed())
            userid = dr.find_element_by_id(IDUserName)
            userid.send_keys(user.uid)

            pwdInput = dr.find_element_by_id (IDPwd)
            pwdInput.send_keys(user.pwd + Keys.RETURN)
            WebDriverWait(dr, 5).until_not(lambda dr: dr.find_element_by_id(IDPwd).is_displayed())
            return True

        except TimeoutException:
            dr.refresh()
            sleep(2)
            self.login()

    def logout(self):
        self.setCurStatus(Status["logout"])
        self.dr.delete_all_cookies()

    def fillUserInfo(self):
        dr = self.dr
        user = self.user
        dr.get(URLOrder)
        trytimes = 1
        self.setCurStatus(Status["preorder"])
        while True:
            try:
                WebDriverWait(dr, 12).until(EC.visibility_of_element_located((By.ID, 'edittextarea')))
                break
            except TimeoutException:
                Status["reorder"][1] = "超时刷新页面 %d次" % trytimes
                self.setCurStatus(Status["reorder"])
                if trytimes > 3:
                    Status["failed"][1] = "获取预约页面失败"
                    self.setCurStatus(Status["failed"])
                    return False
                else:
                    dr.refresh()
                    trytimes += 1
                    continue


        self.setCurStatus(Status["order"])
        while True:
            try:
                userName = dr.find_element_by_id('username')
                userName.send_keys(user.name + Keys.RETURN)

                imail = dr.find_element_by_id('email')
                imail.send_keys(user.email)

                tel = dr.find_element_by_id('tel')
                tel.send_keys(user.tel)
            except ElementNotVisibleException:
                pass

            try:
                e = dr.find_element_by_id('s_province')
                select = Select(e)
                select.select_by_visible_text(user.province)

                e = dr.find_element_by_id('s_city')
                select = Select(e)
                select.select_by_visible_text(user.city)

                e = dr.find_element_by_id('s_dis')
                select = Select(e)
                select.select_by_visible_text(user.district)

            except NoSuchElementException:
                self.setCurStatus(Status["erraddr"])
                return False

            elem = dr.find_element_by_id('edittextarea')
            elem.clear()
            elem.send_keys(user.addr)

            elem = dr.find_element_by_id('postalcode')
            elem.clear()
            elem.send_keys(user.postalcode)

            print("fillUserInfo ok")

            # 翻页到验证界面
            elem = dr.find_element_by_id('checkbox')
            elem.click()

            elem = dr.find_element_by_id('nextStep')
            elem.click()
            WebDriverWait(dr, 5).until_not(lambda dr: dr.find_element_by_id("nextStep").is_displayed())
            break
        return True



    def waitforInputCaptcha(self):
        dr = self.dr
        WebDriverWait(dr, 5).until(lambda dr: dr.find_element_by_id("authCode2").is_displayed())
        self.setCurStatus(Status["inputCaptcha"])
        dr.maximize_window()
        self.captureCaptcha()
        WebDriverWait(dr, 240).until_not(lambda dr: dr.find_element_by_id("authCode2").is_displayed())
        print ("End of waitforInputCaptcha..")

    def captureCaptcha(self):
        # get the image source
        img = self.dr.find_element_by_id('img_captcha2')
        src = img.get_attribute('src')

        print("开始下载")
        # download the image
#         urllib.request.urlretrieve(src, "captcha.png")
        self.dr.save_screenshot("screenshot.png")
        print("下载成功")
    def refreshAuthNunber(self):
        try:
            refreshbtn = self.dr.find_element_by_id('btncode2')  # move_to_element(refreshbtn).
            webdriver.ActionChains(self.dr).click(refreshbtn).perform()
        except ElementNotVisibleException:
                pass

    def order(self):


        dr = self.dr
        if self.login() == False:
            return
        self.fillUserInfo()


        while False:
            try:
                elem = dr.find_element_by_class_name("pro")
                elem.click()
                elem = dr.find_element_by_id('img_captcha2')
                break

            except NoSuchElementException as e:
                print(e)
                dr.refresh()
