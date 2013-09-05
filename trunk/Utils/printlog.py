'''
Created on 2013年9月5日

@author: agz
'''

def status_print(statName, statValue, width = 80, fillChar = '.'):
    outStr = statName + fillChar * (width - len(statName + statValue) - 2) + '[' + statValue + ']'
    print(outStr)

if __name__ == '__main__':
    status_print('check', 'OK')
    pass
