'''
Created on 2013年9月10日

@author: hp41
'''
# encoding: UTF-8
import re

def reTest():
    m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
    lan = re.match(r'''
                        ^(?P<key>[A-Za-z])    # 匹配键值
                        /_(?P<num>\d+)_=      # 匹配中间字符
                        (?P<value>.+)         # 匹配字段值
                    ''', 'S/_11_=取消', re.X)


    lan2 = re.search(r''' \s+|\s$''', 'A/_57_=فق     ط کارت')  # 查询多余的空格
    print()
    print("m.string:", m.string)
    print("m.re:", m.re)
    print("m.pos:", m.pos)
    print("m.endpos:", m.endpos)
    print("m.lastindex:", m.lastindex)
    print("m.lastgroup:", m.lastgroup)

    print("m.group(1,2):", m.group(1, 2))
    print("m.groups():", m.groups())
    print("m.groupdict():", m.groupdict())
    print("m.start(2):", m.start(2))
    print("m.end(2):", m.end(2))
    print("m.span(2):", m.span(2))
    print(r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3'))

    print("\n*************\n lan.groupdict():", lan.groupdict())
    print(lan.groupdict())
    print(lan.string)
    print(r"lan.expand(r'\g<key>/_\g<num>_=\g<value>')", lan.expand(r'\g<key>/_\g<num>_=\g<value>'))

    print("\n*************")
    if lan2:
        print ("match!")
    else:
        print("Not MATCH")

### 输出 ###
# hello
if __name__ == '__main__':
    reTest()
    pass
