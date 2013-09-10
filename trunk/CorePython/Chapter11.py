'''
Created on 2013年9月10日

@author: agz
'''
import re
import time
def tsfunc(func, *nkwargs, **kwargs):
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


@tsfunc
def foo():
    time.sleep(5)
    pass
@tsfunc
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

@tsfunc
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

if __name__ == '__main__':
    tesre()
    pass
