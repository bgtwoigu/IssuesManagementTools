#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on Aug 25, 2015

@author: liuzhsh
'''

import csv

from com.neusoft.utils.Constants import DEBUG, PRISM_SOURCES_FILE
from com.neusoft.utils.Tools import Tools


class CsvFile(object):
    '''
    The csv file operation class.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.__sheet = []
        self.__tools = Tools()

    def read(self, path = PRISM_SOURCES_FILE):
        '''
        read the csv file.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        try:
            with open(path, "rb") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.__sheet.append(row)
            return self.__sheet
        except (IOError, TypeError), e:
            print "[ERROR] %s" % e
            exit()
