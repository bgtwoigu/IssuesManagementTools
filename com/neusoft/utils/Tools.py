#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on Aug 25, 2015

@author: liuzhsh
'''

from inspect import stack


class Tools(object):
    '''
    This is a tools class.
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def getCurrentFunctionName(self):
        '''
        get the current function name.
        '''
        return stack()[1][3]