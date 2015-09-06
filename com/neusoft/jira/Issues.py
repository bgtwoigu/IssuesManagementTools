#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on Aug 25, 2015

@author: liuzhsh
'''

from datetime import datetime
from re import split
from string import atoi

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

        self.__createdId = {}
        self.__getCreatedId()

        self.__jiraStatusId = {}
        self.__getJiraStatusId()

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

    def __getCreatedId(self):
        '''
        get the begin and end time of the created time.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(CREATED_ID_FILE)

        try:
            for row in tempList:
                if not row[VALUE].strip():
                    self.__createdId[row[KEY]] = datetime(atoi(TIME_DICT[row[KEY]][YEAR]), atoi(TIME_DICT[row[KEY]][MONTH]), atoi(TIME_DICT[row[KEY]][DAY]), atoi(TIME_DICT[row[KEY]][HOUR]), atoi(TIME_DICT[row[KEY]][MINUTE]), atoi(TIME_DICT[row[KEY]][SECOND]))
                else:
                    tempSubList = split("[-/]", row[VALUE])
                    self.__createdId[row[KEY]] = datetime(atoi(tempSubList[YEAR]), atoi(tempSubList[MONTH]), atoi(tempSubList[DAY]), atoi(TIME_DICT[row[KEY]][HOUR]), atoi(TIME_DICT[row[KEY]][MINUTE]), atoi(TIME_DICT[row[KEY]][SECOND]))
        except (ValueError), e:
            print "[ERROR] %s" % e
            exit()

        if self.__createdId["BEGIN"] >= self.__createdId["END"]:
            print "[ERROR] THE BEGIN TIME CAN'T BE LATER THAN TEH END TIME."
            exit()

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__createdId.keys():
                print key, "::", self.__createdId[key]
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __getJiraStatusId(self):
        '''
        get the relationship of the key in Jira Status and the PL Status/Assignee/Components.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(JIRA_STATUS_ID_FILE)

        for row in tempList:
            self.__jiraStatusId[row[KEY]] = row[VALUE]

        self.__jiraStatusId[JIRA_OPEN_STATUS] = self.__jiraOpenStatusOperate

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__jiraStatusId.keys():
                print key, "::", self.__jiraStatusId[key]
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

    def __canBeAppend(self, time):
        '''
        determine whether the created time meets the requirements
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if time >= self.__createdId[BEGIN_TIME] and time <= self.__createdId[END_TIME]:
            return True
        else:
            return False

    def __readXlsFiles(self):
        '''
        get the xls file content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__xlsFile = XlsFile()
        tempList = self.__xlsFile.read(self.__jiraFileName, ZERO)

        self.__exportSheet.append(EXPORT_SHEET_TITLE)
        self.__descriptionColumn.append(tempList[KEY][-1])

        for row in range(VALUE, len(tempList)):
            if self.__canBeAppend(tempList[row][CREATED_TIME_COLUMN_NO]):
                tempSubList = []
                for column in range(len(tempList[row]) - DELETE_COLUMN_NUM):
                    tempSubList.append(tempList[row][column])
                self.__exportSheet.append(tempSubList)
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

    def __appendTeamContent(self, row, rowNo):
        '''
        append the content to the Team column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempSubList = row[SUMMARY_COLUMN_NO].upper().split(']')[:5]

        try:
            for key in self.__teamId.keys():
                for r in self.__teamId[key]:
                    for sl in tempSubList:
                        if r.upper() == sl.strip()[1:].lstrip():
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

        tempSubList = row[SUMMARY_COLUMN_NO].upper().split(']')[:5]

        try:
            for key in self.__moduleId.keys():
                for r in self.__moduleId[key]:
                    for sl in tempSubList:
                        if r.upper() == sl.strip()[1:].lstrip():
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

        tempSubList = row[SUMMARY_COLUMN_NO].upper().split(']')[:5]

        try:
            for key in self.__etOrByCaseId.keys():
                for r in self.__etOrByCaseId[key]:
                    for sl in tempSubList:
                        if r.upper() == sl.strip()[1:].lstrip():
                            row.append(r)
                            raise FoundException()
        except FoundException:
            self.__status[rowNo][ET_OR_BY_CASE_COLUMN_NO] = CHANGE_STATUS
        else:
            row.append(BLANK)

    def __appendReporterContent(self, row, rowNo):
        '''
        append the content to the Reporter column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempStr = ''.join(self.__descriptionColumn[rowNo].upper().split("REPORTER:")[1])
        tempStr = ''.join(tempStr.split("\n")[:1]).strip()

        try:
            for key in self.__reporterId.keys():
                for r in self.__reporterId[key]:
                    if tempStr == r.upper():
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

        tempSubList = row[SUMMARY_COLUMN_NO].upper().split(']')[:5]

        try:
            for key in self.__productId.keys():
                for r in self.__productId[key]:
                    for sl in tempSubList:
                        if "[" == sl.strip()[0] and -1 != sl.find(r.upper()):
                            row.append(r)
                            raise FoundException()
        except FoundException:
            self.__status[rowNo][PRODUCT_COLUMN_NO] = CHANGE_STATUS
        else:
            row.append(ERROR)
            self.__status[rowNo][PRODUCT_COLUMN_NO] = ERROR_STATUS

    def __jiraOpenStatusOperate(self, row, rowNo, jiraColumnNo, prismColumnNo):
        '''
        operate jira open status.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if row[CR_ID_COLUMN_NO].isdigit() and self.__prismSheet.has_key(row[CR_ID_COLUMN_NO]):
            self.__status[rowNo][jiraColumnNo] = CHANGE_STATUS
            return self.__prismSheet[row[CR_ID_COLUMN_NO]][prismColumnNo]
        elif row[CR_ID_COLUMN_NO].isdigit() and not self.__prismSheet.has_key(row[CR_ID_COLUMN_NO]):
            self.__status[rowNo][jiraColumnNo] = ERROR_STATUS
            return ERROR
        elif not row[CR_ID_COLUMN_NO].isdigit():
            self.__status[rowNo][jiraColumnNo] = ERROR_STATUS
            return ERROR
        else:
            return BLANK

    def __appendPlStatusContent(self, row, rowNo):
        '''
        append the content to the PL Status column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if JIRA_OPEN_STATUS == row[JIRA_STATUS_COLUMN_NO]:
            row.append(self.__jiraStatusId[row[JIRA_STATUS_COLUMN_NO]](row, rowNo, PL_STATUS_COLUMN_NO, PL_STATUS))
        else:
            row.append(self.__jiraStatusId[row[JIRA_STATUS_COLUMN_NO]])
            self.__status[rowNo][PL_STATUS_COLUMN_NO] = CHANGE_STATUS

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
            if "" == tempStr.lower():
                row.append(BLANK)
            else:
                row.append(tempStr.lower())
                self.__status[rowNo][REPRODUCED_COLUMN_NO] = ERROR_STATUS

    def __appendTagNamesContent(self, row, rowNo):
        '''
        append the content to the TagNames column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if JIRA_OPEN_STATUS == row[JIRA_STATUS_COLUMN_NO]:
            row.append(self.__jiraStatusId[row[JIRA_STATUS_COLUMN_NO]](row, rowNo, TAG_NAMES_COLUMN_NO, TAG_NAMES))

    def __appendModifyContent(self, row, rowNo):
        '''
        append the content to the Modify column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        row.append(BLANK)

    def __updateAssigneeContent(self, row, rowNo):
        '''
        update the content of the Assignee column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if JIRA_OPEN_STATUS == row[JIRA_STATUS_COLUMN_NO]:
            row[ASSIGNEE_COLUMN_NO] = self.__jiraStatusId[row[JIRA_STATUS_COLUMN_NO]](row, rowNo, ASSIGNEE_COLUMN_NO, CR_ASSIGNEE_USER_NAME)

    def __updateComponentsContent(self, row, rowNo):
        '''
        update the content of the Components column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if JIRA_OPEN_STATUS == row[JIRA_STATUS_COLUMN_NO]:
            row[COMPONENTS_COLUMN_NO] = self.__jiraStatusId[row[JIRA_STATUS_COLUMN_NO]](row, rowNo, COMPONENTS_COLUMN_NO, SUB_SYSTEM)

    def __createSheet(self):
        '''
        create a final sheet for writing.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        for row in range(VALUE, len(self.__exportSheet)):
            self.__appendTeamContent(self.__exportSheet[row], row)
            self.__appendModuleContent(self.__exportSheet[row], row)
            self.__appendEtOrByCaseContent(self.__exportSheet[row], row)
            self.__appendReporterContent(self.__exportSheet[row], row)
            self.__appendProductContent(self.__exportSheet[row], row)
            self.__appendPlStatusContent(self.__exportSheet[row], row)
            self.__appendReproducedContent(self.__exportSheet[row], row)
            self.__appendTagNamesContent(self.__exportSheet[row], row)
            self.__appendModifyContent(self.__exportSheet[row], row)
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