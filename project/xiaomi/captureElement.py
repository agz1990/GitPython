#!/bin/python
# coding ---utf-8---

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, \
#     ElementNotVisibleException, TimeoutException
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# browser = webdriver.Firefox()
# browser.save_screenshot('screenshot.png')
# img = browser.find_element_by_xpath('//*[@id="cryptogram"]')
# loc = img.location
#
# image = cv.LoadImage('screenshot.png', True)
# out = cv.CreateImage((150, 60), image.depth, 3)
# cv.SetImageROI(image, (loc['x'], loc['y'], 150, 60))
# cv.Resize(image, out)
# cv.SaveImage('out.jpg', out)

#!/bin/python
# coding ---utf-8---


import urllib.request
from selenium import webdriver

def captureCaptcha(dr):
    # get the image source
    img = dr.find_element_by_xpath('img_captcha2')
    src = img.get_attribute('src')

    # download the image
    urllib.request.urlretrieve(src, "captcha.png")
    print("下载成功")

