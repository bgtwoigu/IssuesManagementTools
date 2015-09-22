#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on Aug 25, 2015

@author: liuzhsh
'''

from xlrd import open_workbook, xldate, XLRDError
from xlwt import easyxf, Workbook
from datetime import datetime

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
        self.__titleStyle = easyxf('pattern: pattern solid, fore_colour gray25; font: bold on;');
        self.__changedStyle = easyxf('pattern: pattern solid, fore_colour green');
        self.__errorStyle = easyxf('pattern: pattern solid, fore_colour red;');
        self.__highlightStyle = easyxf('pattern: pattern solid, fore_colour yellow;');

    def read(self, path=JIRA_SOURCES_FILE, index=ZERO):
        '''
        read the xls content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        try:
            self.__workbook = open_workbook(path)
            self.__worksheet = self.__workbook.sheet_by_index(index)

            for row in range(self.__worksheet.nrows):
                tempList = []
                for column in range(self.__worksheet.ncols):
                    if column in (CREATED_TIME_COLUMN_NO, UPDATED_TIME_COLUMN_NO) and type(self.__worksheet.cell_value(row, column)) is float:
                        tempList.append(xldate.xldate_as_datetime(self.__worksheet.cell(row, column).value, 0))
                    elif column == CR_ID_COLUMN_NO and type(self.__worksheet.cell_value(row, column)) is float:
                        tempList.append(str(int(self.__worksheet.cell_value(row, column))))
                    else:
                        tempList.append(self.__worksheet.cell_value(row, column).encode("utf-8"))
                self.__sheet.append(tempList)
            return self.__sheet
        except (IOError, TypeError, XLRDError), e:
            print "[ERROR] %s" % e
            exit()

    def __write(self, rowNo, columnNo, content, status):
        '''
        write date in the current cell.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if CHANGE_STATUS == status:
            self.__worksheet.write(rowNo, columnNo, content, self.__changedStyle)
        elif ERROR_STATUS == status:
            self.__worksheet.write(rowNo, columnNo, content, self.__errorStyle)
        elif HIGHLIGHT_STATUS == status:
            self.__worksheet.write(rowNo, columnNo, content, self.__highlightStyle)
        else:
            self.__worksheet.write(rowNo, columnNo, content)

    def write(self, sheet="", status="", path=RESULTS_FILE):
        '''
        write content to the xls file.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__workbook = Workbook(encoding = 'utf-8')
        self.__worksheet = self.__workbook.add_sheet('Bug List')

        for column in range(len(sheet[KEY])):
            self.__worksheet.write(KEY, column, str(sheet[KEY][column]), self.__titleStyle)

        for row in range(VALUE, len(sheet)):
            for column in range(len(sheet[row])):
                if type(sheet[row][column]) is datetime:
                    self.__write(row, column, str(sheet[row][column]), status[row][column])
                else:
                    self.__write(row, column, sheet[row][column], status[row][column])

        self.__workbook.save(path)