#!/usr/bin/python3.3

from string import Template

#     前景            背景              颜色
#     ---------------------------------------
#     30                40              黑色
#     31                41              紅色
#     32                42              綠色
#     33                43              黃色
#     34                44              藍色
#     35                45              紫紅色
#     36                46              青藍色
#     37                47              白色
#
#     代码              意义
#     -------------------------
#     0                终端默认设置
#     1                高亮显示
#     4                使用下划线
#     5                闪烁
#     7                反白显示
#     8                不可见

enColor = Template('\033[${attr};4${back};3${font}m${text}\033[1;0m')
baseFont = 30
baseBack = 40
Colors = {'BLACK'   :0,
          'RED'     :1,
          'GREEN'   :2,
          'YELLOW'  :3,
          'BLUE'    :4,
          'AMARANTH':5,
          'ULTRAMARINE':6,
          'WHITE'   :7,
          }
baseAttr = {'Default':0, 'Highlight':1, 'Underline':4, 'Shine':5, 'Invert':7, 'Invisible':8 }
def TestColor():
    for attr in baseAttr:
        for back in Colors:
            for font in Colors:
                style = enColor.substitute(attr = baseAttr[attr], back = Colors[back], font = Colors[font], text = 'Hello world')
                print('%s  <-- Attr:%s Back:%s Text:%s' % (style, attr, back, font))

    pass
if __name__ == '__main__':
    TestColor()
    pass
