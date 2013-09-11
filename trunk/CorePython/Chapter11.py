'''
Created on 2013年9月10日

@author: agz
'''
from urllib.request import urlretrieve
import re
import time

def timeit(func, *nkwargs, **kwargs):
    def wrappedFunc():
        tms = time.clock()
        print('%s()called start...' % (func.__name__))
        func()
        tms = time.clock() - tms
        print('[%s] %s()called end...' % (tms, func.__name__))
    return wrappedFunc



def testit(func, *nkwargs, **kwargs):
    try:
        retval = func(*nkwargs, **kwargs)
        result = (True, retval)
    except Exception as diag:
        result = (False, str(diag))
    return result


@timeit
def foo():
    time.sleep(5)
    pass

@timeit
def test():
    funcs = (int, float)
    vals = (1234, 12.34, '1234', '12.34')
    for eachFunc in funcs:
#             print ('*' * 40)
        for eachVal in vals:
            retval = testit(eachFunc, eachVal)
            if retval[0]:
                print ('%s(%s) = ' % (eachFunc.__name__, repr(eachVal)), retval[1])
            else:
                print('%s(%s) = FAILED:' % (eachFunc.__name__, repr(eachVal)), retval[1])



@timeit
def tesre():
    i = 0
    while (i < 1000000):
        i += 1
        lan = re.match(r'''
                            ^(?P<key>[A-Za-z])    # 匹配键值
                            /_(?P<num>\d+)_=      # 匹配中间字符
                            (?P<value>.+)         # 匹配字段值
                        ''', 'S/_11_=取消', re.X)


        lan2 = re.search(r''' \s+|\s$''', 'S/_11_=取 消')  # 查询多余的空格
        if lan is True:
            continue
        if lan2 is True:
            continue


@timeit
def grabWeb(url='http://www.comptechdoc.org/os/linux/programming/script/linux_pgscriptvariables.html', process=None):
    try:
        retval = urlretrieve(url)[0]
    except IOError:
        retval = None
    if retval:
        f = open(retval)
        for line in f:
            print('>>', line)

    time.sleep(1)
    pass

if __name__ == '__main__':
#     tesre()
    grabWeb()
    pass
