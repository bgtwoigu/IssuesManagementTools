#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on Aug 25, 2015

@author: liuzhsh
'''

import re

from com.neusoft.utils.Constants import *
from com.neusoft.utils.Tools import Tools
from com.neusoft.utils.CsvFile import CsvFile
from com.neusoft.utils.XlsFile import XlsFile

class Issues(object):
    '''
    The Jira issues operation class.
    '''


    def __init__(self, prismFileName, jiraFileName):
        '''
        Constructor
        '''
        self.__tools = Tools()
        
        self.__prismFileName = prismFileName
        self.__jiraFileName = jiraFileName
        self.__csvFile = None
        self.__xlsFile = None

        self.__teamId = {}
        self.__getTeamId()

        self.__moduleId = {}
        self.__getModuleId()

        self.__etOrByCaseId = {}
        self.__getEtOrByCaseId()

        self.__reporterId = {}
        self.__getReporterId()

        self.__productId = {}
        self.__getProductId()

        self.__reproducedId = {}
        self.__getReproducedId()

        self.__prismSheet = {}
        self.__readCsvFiles()

        self.__exportSheet = []
        self.__descriptionColumn = []
        self.__status = []
        self.__readXlsFiles()

    def __getTeamId(self):
        '''
        get the relationship of the key in summary and the team name.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(TEAM_ID_FILE)

        for row in tempList:
            tempSubList = []
            for columnNo in range(VALUE, len(row)):
                tempSubList.append(row[columnNo])
            self.__teamId[row[KEY]] = tempSubList

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__teamId.keys():
                print key, "::", self.__teamId[key]
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __getModuleId(self):
        '''
        get the relationship of the key in summary and the module name.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(MODULE_ID_FILE)

        for row in tempList:
            tempSubList = []
            for columnNo in range(VALUE, len(row)):
                tempSubList.append(row[columnNo])
            self.__moduleId[row[KEY]] = tempSubList

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__moduleId.keys():
                print key, "::", self.__moduleId[key]
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __getEtOrByCaseId(self):
        '''
        get the relationship of the key in summary and the ET or by case.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(ET_OR_BY_CASE_ID_FILE)

        for row in tempList:
            tempSubList = []
            for columnNo in range(VALUE, len(row)):
                tempSubList.append(row[columnNo])
            self.__etOrByCaseId[row[KEY]] = tempSubList

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__etOrByCaseId.keys():
                print key, "::", self.__etOrByCaseId[key]
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __getReporterId(self):
        '''
        get the relationship of reporter's name in English and Chinese.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(REPORTER_ID_FILE)

        for row in tempList:
            tempSubList = []
            for columnNo in range(VALUE, len(row)):
                tempSubList.append(row[columnNo])
            self.__reporterId[row[KEY]] = tempSubList

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__reporterId.keys():
                print key, "::", self.__reporterId[key]
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __getProductId(self):
        '''
        get the relationship of the key in summary and the product.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(PRODUCT_ID_FILE)

        for row in tempList:
            tempSubList = []
            for columnNo in range(VALUE, len(row)):
                tempSubList.append(row[columnNo])
            self.__productId[row[KEY]] = tempSubList

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__productId.keys():
                print key, "::", self.__productId[key]
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __getReproducedId(self):
        '''
        get the relationship of the key in summary and the reproduced on 8952.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(REPRODUCED_ID_FILE)

        for row in tempList:
            tempSubList = []
            for columnNo in range(VALUE, len(row)):
                tempSubList.append(row[columnNo])
            self.__reproducedId[row[KEY]] = tempSubList

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__reproducedId.keys():
                print key, "::", self.__reproducedId[key]
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __readCsvFiles(self):
        '''
        get the useful csv file content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(self.__prismFileName)

        for row in range(VALUE, len(tempList)):
            tempSubDict = {}
            for column in range(VALUE, len(tempList[row])):
                tempSubDict[tempList[KEY][column]] = tempList[row][column]
            self.__prismSheet[tempList[row][KEY]] = tempSubDict

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__prismSheet.keys():
                print "MAIN_KEY ::", key 
                for subKey in self.__prismSheet[key]:
                    print subKey, "::", self.__prismSheet[key][subKey]
                print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __readXlsFiles(self):
        '''
        get the xls file content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__xlsFile = XlsFile()
        tempList = self.__xlsFile.read(self.__jiraFileName, ZERO)

        self.__exportSheet = [[] for _ in range(len(tempList))]
        for row in range(len(tempList)):
            tempSubList = []
            for column in range(len(tempList[row]) - DELETE_COLUMN_NUM):
                tempSubList.append(tempList[row][column])
            self.__exportSheet[row] = tempSubList
            self.__descriptionColumn.append(tempList[row][-1])

        self.__status = [[""] * COLUMN_SUM for _ in range(len(tempList))]

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for r in range(len(self.__exportSheet)):
                for c in range(len(self.__exportSheet[r])):
                    print self.__exportSheet[r][c]
                print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for d in self.__descriptionColumn:
                print d
                print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __appendTitle(self):
        '''
        append the new title to new sheet.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__exportSheet[KEY].extend(ADDITIONAL_TITLE)

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print self.__exportSheet[KEY]
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __appendTeamContent(self, row, rowNo):
        '''
        append the content to the Team column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempStr = ''.join(row[SUMMARY_COLUMN_NO].upper().split(']')[:5])

        try:
            for key in self.__teamId.keys():
                for r in self.__teamId[key]:
                    if -1 != tempStr.find(r.upper()):
                        row.append(key)
                        raise FoundException()
        except FoundException:
            self.__status[rowNo][TEAM_COLUMN_NO] = CHANGE_STATUS
        else:
            row.append(ERROR)
            self.__status[rowNo][TEAM_COLUMN_NO] = ERROR_STATUS

    def __appendModuleContent(self, row, rowNo):
        '''
        append the content to the Module column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempStr = ''.join(row[SUMMARY_COLUMN_NO].upper().split(']')[:5])

        try:
            for key in self.__moduleId.keys():
                for r in self.__moduleId[key]:
                    if -1 != tempStr.find(r.upper()):
                        row.append(r)
                        raise FoundException()
        except FoundException:
            self.__status[rowNo][MODULE_COLUMN_NO] = CHANGE_STATUS
        else:
            row.append(ERROR)
            self.__status[rowNo][MODULE_COLUMN_NO] = ERROR_STATUS

    def __appendEtOrByCaseContent(self, row, rowNo):
        '''
        append the content to the ET/by case column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempStr = ''.join(row[SUMMARY_COLUMN_NO].upper().split(']')[:5])

        try:
            for key in self.__etOrByCaseId.keys():
                for r in self.__etOrByCaseId[key]:
                    if -1 != tempStr.find(r.upper()):
                        row.append(r)
                        raise FoundException()
        except FoundException:
            self.__status[rowNo][ET_OR_BY_CASE_COLUMN_NO] = CHANGE_STATUS
        else:
            row.append(ERROR)
            self.__status[rowNo][ET_OR_BY_CASE_COLUMN_NO] = ERROR_STATUS

    def __appendReporterContent(self, row, rowNo):
        '''
        append the content to the Reporter column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        try:
            for key in self.__reporterId.keys():
                for r in self.__reporterId[key]:
                    if row[REPORTER_1_COLUMN_NO].upper() == r.upper():
                        row.append(key)
                        raise FoundException()
        except FoundException:
            self.__status[rowNo][REPORTER_2_COLUMN_NO] = CHANGE_STATUS
        else:
            row.append(ERROR)
            self.__status[rowNo][REPORTER_2_COLUMN_NO] = ERROR_STATUS

    def __appendProductContent(self, row, rowNo):
        '''
        append the content to the Product column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempStr = ''.join(row[SUMMARY_COLUMN_NO].upper().split(']')[:5])

        try:
            for key in self.__productId.keys():
                for r in self.__productId[key]:
                    if -1 != tempStr.find(r.upper()):
                        row.append(r)
                        raise FoundException()
        except FoundException:
            self.__status[rowNo][PRODUCT_COLUMN_NO] = CHANGE_STATUS
        else:
            row.append(ERROR)
            self.__status[rowNo][PRODUCT_COLUMN_NO] = ERROR_STATUS

    def __appendPlStatusContent(self, row, rowNo):
        '''
        append the content to the PL Status column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if "Preliminary Analysis" == row[JIRA_STATUS_COLUMN_NO]:
            row.append("Triage")
            self.__status[rowNo][PL_STATUS_COLUMN_NO] = CHANGE_STATUS
        elif "Closed" == row[JIRA_STATUS_COLUMN_NO]:
            row.append("Closed")
            self.__status[rowNo][PL_STATUS_COLUMN_NO] = CHANGE_STATUS
        elif "Open" == row[JIRA_STATUS_COLUMN_NO] and row[CR_ID_COLUMN_NO].isdigit() and self.__prismSheet.has_key(row[CR_ID_COLUMN_NO]):
            row.append(self.__prismSheet[row[CR_ID_COLUMN_NO]][PL_STATUS])
            self.__status[rowNo][PL_STATUS_COLUMN_NO] = CHANGE_STATUS
        elif "Open" == row[JIRA_STATUS_COLUMN_NO] and row[CR_ID_COLUMN_NO].isdigit() and not self.__prismSheet.has_key(row[CR_ID_COLUMN_NO]):
            row.append(ERROR)
            self.__status[rowNo][PL_STATUS_COLUMN_NO] = ERROR_STATUS
        elif "Open" == row[JIRA_STATUS_COLUMN_NO] and not row[CR_ID_COLUMN_NO].isdigit():
            row.append(ERROR)
            self.__status[rowNo][PL_STATUS_COLUMN_NO] = ERROR_STATUS
        else:
            row.append(BLANK)

    def __appendReproducedContent(self, row, rowNo):
        '''
        append the content to the Reproduced on 8952 column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempStr = ''.join(self.__descriptionColumn[rowNo].upper().split("[ADDITIONAL")[1:])

        try:
            for key in self.__reproducedId.keys():
                for r in self.__reproducedId[key]:
                    if -1 != tempStr.find(r.upper()):
                        row.append(key)
                        raise FoundException()
        except FoundException:
            self.__status[rowNo][REPRODUCED_COLUMN_NO] = CHANGE_STATUS
        else:
            row.append(ERROR)
            self.__status[rowNo][REPRODUCED_COLUMN_NO] = ERROR_STATUS

    def __updateAssigneeContent(self, row, rowNo):
        '''
        update the content of the Assignee column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if "Open" == row[JIRA_STATUS_COLUMN_NO] and row[CR_ID_COLUMN_NO].isdigit() and self.__prismSheet.has_key(row[CR_ID_COLUMN_NO]):
            row[ASSIGNEE_COLUMN_NO] = self.__prismSheet[row[CR_ID_COLUMN_NO]][CR_ASSIGNEE_USER_NAME]
            self.__status[rowNo][ASSIGNEE_COLUMN_NO] = CHANGE_STATUS
        elif "Open" == row[JIRA_STATUS_COLUMN_NO] and row[CR_ID_COLUMN_NO].isdigit() and not self.__prismSheet.has_key(row[CR_ID_COLUMN_NO]):
            row[ASSIGNEE_COLUMN_NO] = ERROR
            self.__status[rowNo][ASSIGNEE_COLUMN_NO] = ERROR_STATUS

    def __updateComponentsContent(self, row, rowNo):
        '''
        update the content of the Components column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if "Open" == row[JIRA_STATUS_COLUMN_NO] and row[CR_ID_COLUMN_NO].isdigit() and self.__prismSheet.has_key(row[CR_ID_COLUMN_NO]):
            row[COMPONENTS_COLUMN_NO] = self.__prismSheet[row[CR_ID_COLUMN_NO]][SUB_SYSTEM]
            self.__status[rowNo][COMPONENTS_COLUMN_NO] = CHANGE_STATUS
        elif "Open" == row[JIRA_STATUS_COLUMN_NO] and row[CR_ID_COLUMN_NO].isdigit() and not self.__prismSheet.has_key(row[CR_ID_COLUMN_NO]):
            row[COMPONENTS_COLUMN_NO] = ERROR
            self.__status[rowNo][COMPONENTS_COLUMN_NO] = ERROR_STATUS
        else:
            row[COMPONENTS_COLUMN_NO] = BLANK

    def __createSheet(self):
        '''
        create a final sheet for writing.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__appendTitle()
        for row in range(VALUE, len(self.__exportSheet)):
            self.__appendTeamContent(self.__exportSheet[row], row)
            self.__appendModuleContent(self.__exportSheet[row], row)
            self.__appendEtOrByCaseContent(self.__exportSheet[row], row)
            self.__appendReporterContent(self.__exportSheet[row], row)
            self.__appendProductContent(self.__exportSheet[row], row)
            self.__appendPlStatusContent(self.__exportSheet[row], row)
            self.__appendReproducedContent(self.__exportSheet[row], row)
            self.__updateAssigneeContent(self.__exportSheet[row], row)
            self.__updateComponentsContent(self.__exportSheet[row], row)

    def __writeXlsFiles(self):
        '''
        get the xls file content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__xlsFile = XlsFile()
        self.__xlsFile.write(self.__exportSheet, self.__status)

    def exportIssues(self):
        '''
        export all issues.
        '''
        self.__createSheet()
        self.__writeXlsFiles()