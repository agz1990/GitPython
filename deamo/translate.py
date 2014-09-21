# import lxml  
from urllib.error import HTTPError, URLError
import urllib.parse
import urllib.request
#  
# class URLLister(SGMLParser):
#     def __init__(self, result):
#         SGMLParser.__init__(self)
#         self.result = result
#         self.open = False
#     def start_div(self, attrs):
#         id = [v for k, v in attrs if k == 'id']
#         if 'tts_button' in id:
#             self.open = True
#     def handle_data(self, text):
#         if self.open:
#             self.result.append(text)
#             self.open = False
 
def translate(text):
    out = []     
    values = {'hl':'zh-CN', 'ie':'UTF-8', 'text':'hello ', 'langpair':"en"}  
    url = 'http://translate.google.cn/translate_t'  
    user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)"
    headers = { 'User-Agent' : user_agent }
    data = urllib.parse.urlencode(values)
    req = urllib.request.Request(url, data.encode(encoding='UTF8'), headers)
#     response = urllib.request.urlopen(req)
#     the_page = response.read()
#     print(response.read())  
    
    
    try:
        response = urllib.request.urlopen(req)   # open=urlopen
    except HTTPError as e:
        print('Error code:', e.code) 
    except URLError as e:
        print('Reason', e.reason)
    the_page = response.read()
    with open('gool.html', 'bw') as f:
        f.write(the_page)
    print(the_page)    
#     parser = URLLister(out)
#     parser.feed(response.read())  
#     parser.close()
#     result = out[0]   
#     return result  
 
translate('hello')



# from urllib.error import URLError, HTTPError
# import urllib.request
# import urllib.parse
# url = 'http://www.baidu.com/s'
# values = {'wd':'python',
#         'opt-webpage':'on',
#         'ie':'gbk'}
# url_values = urllib.parse.urlencode(values)
# # print(url_values)
# 
# url_values = url_values.encode(encoding='UTF8')
# full_url = urllib.request.Request(url, url_values)
# # or ony one sentense:full_url=url+'?'+url_values
# 
# response = None
# try:
#     response = urllib.request.urlopen(full_url)   # open=urlopen
# except HTTPError as e:
#     print('Error code:', e.code) 
# except URLError as e:
#     print('Reason', e.reason)
# the_page = response.read()
# print(the_page)
