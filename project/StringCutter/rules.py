
import re
from configparser import ConfigParser

class Rules(ConfigParser):
    '''
    classdocs
    '''
    def __init__(self, rulesfile='cutter.ini',):
        '''
        Constructor
        '''
        super(Rules, self).__init__()
        self.read(rulesfile, 'utf-8')
        self.order = self.get('Default', 'ruleOrder').split(',')
#         print(self.get('Default', 'ruleOrder').split(','))

    def getOrder(self):
        return  self.order

    def report(self, m, text=''):
        if m :

            if m.groupdict():
                print(m.groupdict())
            print('***   Mach   ***  String:%s With:^^^%s^^^ ...' % (m.string, m.group()))
        else:
            print('**** NotMach ***  String:%s' % text)


    def Test(self, regExp, text):
        m = re.search(regExp, text, re.X)
        self.report(m, text)
        return bool(m)

    def procCheck(self, cell):
        for rule in self.getOrder():
            pattern = self.get(rule, pattern)

        pass


