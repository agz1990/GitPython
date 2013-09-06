'''
Created on 2013年9月5日

@author: hp41
'''

import Rule

def safe_float(obj): 
    try: 
        retval = float(obj) 
    except ValueError: 
        retval = 'could not convert non-number to float' 
    except TypeError: 
        retval = 'object type cannot be converted to float' 
    return retval 

if __name__ == '__main__':
    Rule.Details()
    try:
        f = open('xxx','r')
    except IOError as e:
        print('could not open file:')
    else:
        pass
    
