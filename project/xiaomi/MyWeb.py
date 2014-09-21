#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, \
    ElementNotVisibleException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep


# 登录的网站
URLLogin = 'https://account.xiaomi.com/pass/serviceLogin'

# 预约的网站
URLOrder = "http://a.hd.xiaomi.com/register/book/a/35"
IDUserName = 'username'
IDPwd = "userPwd"
class MiWeb():
    def __init__(self, user, browser = None, processbar = None):
        self.user = user
        if browser == None:
            browser = webdriver.Firefox()
        self.dr = browser

    def login(self):
        dr = self.dr
        user = self.user

        try:
            dr.get(URLLogin)
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


    def fillUserInfo(self):
        dr = self.dr
        user = self.user

        dr.get(URLOrder)
        while True:
            try:
                sleep(1)
                WebDriverWait(dr, 12).until(EC.visibility_of_element_located((By.ID, 'edittextarea')))
                break
            except TimeoutException:
                dr.refresh()
                print("fillUserInfo TimeoutException")
                continue

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
                print('地址信息填写出错')
                return False

            elem = dr.find_element_by_id('edittextarea')
            elem.send_keys(user.addr)

            elem = dr.find_element_by_id('postalcode')
            elem.send_keys(user.postalcode)

            print("fillUserInfo ok")
            break

        return True


    def order(self):
        dr = self.dr
        if self.login() == False:
            return

        if self.fillUserInfo():


            elem = dr.find_element_by_id('checkbox')
            elem.click()

            elem = dr.find_element_by_id('nextStep')

            js = '''
            var p2 = document.getElementById("formBox");
            p2.parentNode.removeChild(p2);
            '''
            elem.click()



        while False:
            try:
                elem = dr.find_element_by_class_name("pro")
                elem.click()
                elem = dr.find_element_by_id('img_captcha2')
                break

            except NoSuchElementException as e:
                print(e)
                dr.refresh()



