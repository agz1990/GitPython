'''
Created on 2013年10月15日

@author: hp41
'''
import configparser
config = configparser.ConfigParser()

config['DEFAULT'] = {'ServerAliveInterval': '42',
                      'Compression': 'yes', 'CompressionLevel': '9'}
config['bitbucket.org'] = {}
topsecret = config['topsecret.server.com'] = {}
config['bitbucket.org']['User'] = 'hg'
topsecret['Port'] = '50022'   # mutates the parser
topsecret['ForwardX11'] = 'no'   # same here
config['DEFAULT']['ForwardX11'] = 'yes'
with open('example.ini', 'w') as configfile:
    config.write(configfile)

if __name__ == '__main__':
    pass
