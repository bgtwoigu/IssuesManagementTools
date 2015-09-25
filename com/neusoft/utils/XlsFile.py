#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on Aug 25, 2015

@author: liuzhsh
'''

from xlrd import open_workbook, xldate, XLRDError
from xlwt import easyxf, Workbook

from com.neusoft.utils.Tools import Tools
from com.neusoft.utils.Constants import *

class XlsFile(object):
    '''
    The xls file operation class.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__tools = Tools()
        self.__sheet = []
        self.__workbook = None
        self.__worksheet = None
        self.__styleOperator = {TITLE_STATUS : easyxf('pattern: pattern solid, fore_colour gray25; font: bold on;'),
                                CHANGE_STATUS : easyxf('pattern: pattern solid, fore_colour green'),
                                ERROR_STATUS : easyxf('pattern: pattern solid, fore_colour red;'),
                                HIGHLIGHT_STATUS : easyxf('pattern: pattern solid, fore_colour yellow;'),
                                WHITE_STATUS : easyxf('')}
        self.__typeOperator = {EMPTY_TYPE : self.__getEmptyType,
                               TEXT_TYEP : self.__getTextType,
                               NUMBER_TYPE : self.__getNumberType,
                               DATE_TYPE : self.__getDateType,
                               BOOLEAN_TYPE : self.__getBooleanType,
                               ERROR_TYPE : self.__getErrorType,
                               BLANK_TYPE : self.__getBlankType}

    def __getEmptyType(self, rowNo, columnNo):
        '''
        return the empty type content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        return self.__worksheet.cell_value(rowNo, columnNo).encode("utf-8")

    def __getTextType(self, rowNo, columnNo):
        '''
        return the text type content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        return self.__worksheet.cell_value(rowNo, columnNo).encode("utf-8")

    def __getNumberType(self, rowNo, columnNo):
        '''
        return the number type content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        return str(int(self.__worksheet.cell_value(rowNo, columnNo)))

    def __getDateType(self, rowNo, columnNo):
        '''
        read the date type content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        return xldate.xldate_as_datetime(self.__worksheet.cell(rowNo, columnNo).value, 0)

    def __getBooleanType(self, rowNo, columnNo):
        '''
        return the boolean type content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        return self.__worksheet.cell_value(rowNo, columnNo).encode("utf-8")

    def __getErrorType(self, rowNo, columnNo):
        '''
        return the error type content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        return self.__worksheet.cell_value(rowNo, columnNo).encode("utf-8")

    def __getBlankType(self, rowNo, columnNo):
        '''
        return the blank type content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        return self.__worksheet.cell_value(rowNo, columnNo).encode("utf-8")

    def read(self, path=JIRA_SOURCES_FILE, index=ZERO):
        '''
        read the xls content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        try:
            self.__workbook = open_workbook(path)
            self.__worksheet = self.__workbook.sheet_by_index(index)

            for rowNo in range(self.__worksheet.nrows):
                tempList = []
                for columnNo in range(self.__worksheet.ncols):
                    tempList.append(self.__typeOperator[self.__worksheet.cell_type(rowNo, columnNo)](rowNo, columnNo))
                self.__sheet.append(tempList)
            return self.__sheet
        except (IOError, TypeError, XLRDError), e:
            print "[ERROR] %s" % e
            exit()

    def write(self, sheet="", path = RESULTS_FILE):
        '''
        write content to the xls file.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__workbook = Workbook(encoding = 'utf-8')
        self.__worksheet = self.__workbook.add_sheet('Bug List')

        for rowNo in range(len(sheet)):
            for columnNo in range(len(sheet[rowNo])):
                self.__worksheet.write(rowNo, columnNo, str(sheet[rowNo][columnNo][CONTENT]), self.__styleOperator[sheet[rowNo][columnNo][VALUE]])

        self.__workbook.save(path)
