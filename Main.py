#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on Aug 25, 2015

@author: liuzhsh
'''

from optparse import OptionParser
from os import getcwd
from glob import glob
from types import StringType

from com.neusoft.utils.Constants import *
from com.neusoft.jira.Issues import Issues

def optionParser():
    '''
    get options.
    '''
    parser = OptionParser()
    parser.add_option("-p", "--path", dest="path", action="store", default="%s/Sources" % getcwd(), help="This is a path of sources files.")
    options, _ = parser.parse_args()
    if DEBUG:
        print "FILE_PATH : %s" % options.path
    return options.path

def main():
    '''
    the main function.
    '''
    options = optionParser()

    #get prism export file path.
    prismFileName = None
    for fileName in glob("%s/*.csv" % options):
        if type(fileName) is StringType and "PrismSearchResults" in fileName:
            if DEBUG:
                print "FILE_NAME : %s" % fileName
            prismFileName = fileName
            break

    #get jira export file path.
    jiraFileName = None
    for fileName in glob("%s/*.xls" % options):
        if type(fileName) is StringType and "SearchRequest" in fileName:
            if DEBUG:
                print "FILE_NAME : %s" % fileName
            jiraFileName = fileName
            break

    if prismFileName is None or jiraFileName is None:
        print "ERROR: the sources files do not be provided."
        return

    issues = Issues(prismFileName, jiraFileName)
    issues.exportIssues()
    print "Export finished."

if __name__ == '__main__':
    main()
