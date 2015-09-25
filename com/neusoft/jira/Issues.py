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

        self.__createdId = {}
        self.__getCreatedId()

        self.__etOrByCaseId = {}
        self.__getEtOrByCaseId()

        self.__exportResultsTitleId = []
        self.__getExportResultsTitleId()

        self.__jiraStatusId = {}
        self.__getJiraStatusId()

        self.__moduleId = {}
        self.__getModuleId()

        self.__plStatusId = {}
        self.__getPlStatusId()

        self.__productId = {}
        self.__getProductId()

        self.__reporterId = {}
        self.__getReporterId()

        self.__reproducedId = {}
        self.__getReproducedId()

        self.__teamId = {}
        self.__getTeamId()

        self.__prismTitleId = {}
        self.__prismSheet = {}
        self.__readCsvFiles()

        self.__jiraTitleId = {}
        self.__jiraSheet = []
        self.__readXlsFiles()

        self.__exportSheet = []
        self.__descriptionColumn = []
        self.__status = []

        self.__columnOperator = {'Issue Type' : self.__insertIssueType,
                                 'Key' : self.__insertKey,
                                 'Summary' : self.__insertSummary,
                                 'Assignee' : self.__insertAssignee,
                                 'Reporter from JIRA' : self.__insertReporterFromJira,
                                 'JIRA Status' : self.__insertJiraStatus,
                                 'Created' : self.__insertCreated,
                                 'Updated' : self.__insertUpdated,
                                 'RCA' : self.__insertRca,
                                 'CRID' : self.__insertCrid,
                                 'Issue Close Reason' : self.__insertIssueCloseReason,
                                 'Subsystem' : self.__insertSubsystem,
                                 'Team' : self.__insertTeam,
                                 'Module' : self.__insertModule,
                                 'ET/by case' : self.__insertEtorByCase,
                                 'Reporter' : self.__insertReporter,
                                 'Product' : self.__insertProduct,
                                 'PL Status' : self.__insertPlStatus,
                                 'Reproduced on 8952' : self.__insertReproducedOn8952,
                                 'Issue Priority in Prism' : self.__insertIssuePriorityInPrism,
                                 'TagNames' : self.__insertTagNames,
                                 'TestCaseNumber' : self.__insertTestCaseNumber,
                                 'CR Severity' : self.__insertCrSeverity,
                                 'JIRA Severity' : self.__insertJiraSeverity}

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

    def __getExportResultsTitleId(self):
        '''
        get the title name and the order of the title name.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(EXPORT_RESULTS_TITLE_ID_FILE)

        for tempSubList in tempList:
            self.__exportResultsTitleId.append(tempSubList[KEY])

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print self.__exportResultsTitleId
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

        self.__jiraStatusId[JIRA_OPEN_STATUS] = self.__getPrismContent

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__jiraStatusId.keys():
                print key, "::", self.__jiraStatusId[key]
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

    def __getPlStatusId(self):
        '''
        get the priority of the PL Status.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(PL_STATUS_ID_FILE)

        for row in tempList:
            self.__plStatusId[row[KEY]] = row[VALUE]

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__plStatusId.keys():
                print key, "::", self.__plStatusId[key]
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

    def __readCsvFiles(self):
        '''
        get the useful csv file content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__csvFile = CsvFile()
        tempList = self.__csvFile.read(self.__prismFileName)

        for columnNo, titleName in enumerate(tempList[KEY]):
            self.__prismTitleId[titleName] = columnNo

        for rowNo in range(VALUE, len(tempList)):
            if not self.__prismSheet.has_key(tempList[rowNo][KEY]):
                tempSubDict = {}
                for columnNo in range(VALUE, len(tempList[rowNo])):
                    tempSubDict[tempList[KEY][columnNo]] = tempList[rowNo][columnNo]
                self.__prismSheet[tempList[rowNo][KEY]] = tempSubDict
            elif self.__plStatusId[tempList[rowNo][self.__prismTitleId[PL_STATUS]]].isdigit() and self.__plStatusId[self.__prismSheet[tempList[rowNo][KEY]][PL_STATUS]].isdigit() and atoi(self.__plStatusId[tempList[rowNo][self.__prismTitleId[PL_STATUS]]]) < atoi(self.__plStatusId[self.__prismSheet[tempList[rowNo][KEY]][PL_STATUS]]):
                tempSubDict = {}
                for columnNo in range(VALUE, len(tempList[rowNo])):
                    tempSubDict[tempList[KEY][columnNo]] = tempList[rowNo][columnNo]
                self.__prismSheet[tempList[rowNo][KEY]] = tempSubDict

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__prismTitleId.keys():
                print key, self.__prismTitleId[key]
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
        tempList = self.__xlsFile.read(self.__jiraFileName, XLS_SHEET_INDEX)

        for columnNo, titleName in enumerate(tempList[KEY]):
            self.__jiraTitleId[titleName] = columnNo

        for rowNo in range(VALUE, len(tempList)):
            if self.__canBeAppend(tempList[rowNo][self.__jiraTitleId[JIRA_CREATED]]):
                tempSubDict = {}
                for columnNo in range(len(tempList[rowNo])):
                    tempSubDict[tempList[KEY][columnNo]] = tempList[rowNo][columnNo]
                self.__jiraSheet.append(tempSubDict)

        if DEBUG:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for key in self.__jiraTitleId.keys():
                print "%s :: %s" % ( key, self.__jiraTitleId[key])
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            for j in self.__jiraSheet:
                for k in j.keys():
                    print "%s :: %s" % (k, j[k])
                print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    def __getPrismContent(self, crid, column):
        '''
        get prism content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if crid.isdigit() and self.__prismSheet.has_key(crid):
            return [self.__prismSheet[crid][column], CHANGE_STATUS]
        elif crid.isdigit() and not self.__prismSheet.has_key(crid):
            return [ERROR, ERROR_STATUS]
        else:
            return [BLANK, WHITE_STATUS]

    def __insertIssueType(self, importRow, exportRow):
        '''
        insert Issue Type column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_ISSUE_TYPE], WHITE_STATUS])

    def __insertKey(self, importRow, exportRow):
        '''
        insert key column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_KEY], WHITE_STATUS])

    def __insertSummary(self, importRow, exportRow):
        '''
        insert Summary column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_SUMMARY], WHITE_STATUS])

    def __insertAssignee(self, importRow, exportRow):
        '''
        insert Assignee column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if JIRA_OPEN_STATUS == importRow[JIRA_STATUS]:
            exportRow.append(self.__jiraStatusId[JIRA_OPEN_STATUS](importRow[JIRA_CR_ID], CR_ASSIGNEE_USER_NAME))
        else:
            exportRow.append([importRow[JIRA_ASSIGNEE], WHITE_STATUS])

    def __insertReporterFromJira(self, importRow, exportRow):
        '''
        insert Reporter column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_REPORTER], WHITE_STATUS])

    def __insertJiraStatus(self, importRow, exportRow):
        '''
        insert JIRA Status column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_STATUS], WHITE_STATUS])

    def __insertCreated(self, importRow, exportRow):
        '''
        insert Created column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_CREATED], WHITE_STATUS])

    def __insertUpdated(self, importRow, exportRow):
        '''
        insert Updated column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_UPDATED], WHITE_STATUS])

    def __insertRca(self, importRow, exportRow):
        '''
        insert RCA column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_RCA], WHITE_STATUS])

    def __insertCrid(self, importRow, exportRow):
        '''
        insert CRID column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_CR_ID], WHITE_STATUS])

    def __insertIssueCloseReason(self, importRow, exportRow):
        '''
        insert Issue Close Reason column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_ISSUE_CLOSE_REASON], WHITE_STATUS])

    def __insertSubsystem(self, importRow, exportRow):
        '''
        insert Subsystem column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if JIRA_OPEN_STATUS == importRow[JIRA_STATUS]:
            exportRow.append(self.__jiraStatusId[JIRA_OPEN_STATUS](importRow[JIRA_CR_ID], SUB_SYSTEM))
        else:
            exportRow.append([importRow[JIRA_COMPONENTS], WHITE_STATUS])

    def __insertTeam(self, importRow, exportRow):
        '''
        insert Team column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempSubList = importRow[JIRA_SUMMARY].upper().split(']')[:5]

        for key in self.__teamId.keys():
            for r in self.__teamId[key]:
                for sl in tempSubList:
                    if r.upper() == sl.strip().lstrip('['):
                        exportRow.append([key, CHANGE_STATUS])
                        return

        exportRow.append([ERROR, ERROR_STATUS])

    def __insertModule(self, importRow, exportRow):
        '''
        insert Module column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempSubList = importRow[JIRA_SUMMARY].upper().split(']')[:5]

        for key in self.__moduleId.keys():
            for r in self.__moduleId[key]:
                for sl in tempSubList:
                    if r.upper() == sl.strip().lstrip('['):
                        exportRow.append([r, CHANGE_STATUS])
                        return

        exportRow.append([ERROR, ERROR_STATUS])

    def __insertEtorByCase(self, importRow, exportRow):
        '''
        insert ET/by case column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempSubList = importRow[JIRA_SUMMARY].upper().split(']')[:5]

        for key in self.__etOrByCaseId.keys():
            for r in self.__etOrByCaseId[key]:
                for sl in tempSubList:
                    if r.upper() == sl.strip().lstrip('['):
                        exportRow.append([key, CHANGE_STATUS])
                        return

        exportRow.append([BLANK, WHITE_STATUS])

    def __insertReporter(self, importRow, exportRow):
        '''
        insert Reporter column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempList = importRow[JIRA_DESCRIPTION].split("\n")
        tempStr = None
        for r in tempList:
            if r.find("@") >= 0:
                tempStr = r.split(":")[1]
                break

        for key in self.__reporterId.keys():
            for r in self.__reporterId[key]:
                if tempStr is not None and tempStr.strip().upper() == r.upper():
                    exportRow.append([key, CHANGE_STATUS])
                    return

        exportRow.append([ERROR, ERROR_STATUS])

    def __insertProduct(self, importRow, exportRow):
        '''
        insert Product column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempSubList = importRow[JIRA_SUMMARY].upper().split(']')[:5]

        for key in self.__productId.keys():
            for r in self.__productId[key]:
                for sl in tempSubList:
                    if "[" == sl.strip()[0] and sl.find(r.upper()) >= 0:
                        exportRow.append([r, CHANGE_STATUS])
                        return

        exportRow.append([ERROR, ERROR_STATUS])

    def __insertPlStatus(self, importRow, exportRow):
        '''
        insert PL Status column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        if JIRA_OPEN_STATUS == importRow[JIRA_STATUS]:
            exportRow.append(self.__jiraStatusId[JIRA_OPEN_STATUS](importRow[JIRA_CR_ID], PL_STATUS))
        else:
            exportRow.append([self.__jiraStatusId[importRow[JIRA_STATUS]], CHANGE_STATUS])

    def __insertReproducedOn8952(self, importRow, exportRow):
        '''
        insert Reproduced on 8952 column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempStr = ''.join(importRow[JIRA_DESCRIPTION].upper().split("[ADDITIONAL")[1:])

        for key in self.__reproducedId.keys():
            for r in self.__reproducedId[key]:
                if tempStr.find(r.upper()) >= 0:
                    exportRow.append([key, CHANGE_STATUS])
                    return

        if "" == tempStr.lower():
            exportRow.append([BLANK, WHITE_STATUS])
        else:
            exportRow.append([tempStr.lower().lstrip(']').strip(), ERROR_STATUS])

    def __insertIssuePriorityInPrism(self, importRow, exportRow):
        '''
        insert Issue Priority in Prism column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempList = self.__getPrismContent(importRow[JIRA_CR_ID], CR_PRIORITY)

        if BLANK == tempList[CONTENT]:
            exportRow.append([importRow[JIRA_ISSUE_PRIORITY_IN_PRISM], WHITE_STATUS])
        else:
            exportRow.append(tempList)

    def __insertTagNames(self, importRow, exportRow):
        '''
        insert Tag Names column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempList = self.__getPrismContent(importRow[JIRA_CR_ID], TAG_NAMES)

        for r in TAG_NAMES_IDENTIFIER:
            if tempList[CONTENT].upper().find(r) >= 0:
                exportRow.append([tempList[CONTENT], HIGHLIGHT_STATUS])
                return

        exportRow.append(tempList)

    def __insertTestCaseNumber(self, importRow, exportRow):
        '''
        insert Test Case Number column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempTagNameList = self.__getPrismContent(importRow[JIRA_CR_ID], TAG_NAMES)
        tempTestCaseNumberList = self.__getPrismContent(importRow[JIRA_CR_ID], TEST_CASE_NUMBER)

        if tempTagNameList[CONTENT].upper().find(TEST_CASE_NUMBER_IDENTIFIER) >= 0 and 'NULL' != tempTestCaseNumberList[CONTENT].upper():
            exportRow.append([tempTestCaseNumberList[CONTENT], ERROR_STATUS])
        elif '' != tempTagNameList[CONTENT] and tempTagNameList[CONTENT].upper().find(TEST_CASE_NUMBER_IDENTIFIER) < 0 and ('NULL' == tempTestCaseNumberList[CONTENT].upper() or '' == tempTestCaseNumberList[CONTENT].upper()):
            exportRow.append([tempTestCaseNumberList[CONTENT], ERROR_STATUS])
        else:
            exportRow.append(tempTestCaseNumberList)

    def __insertCrSeverity(self, importRow, exportRow):
        '''
        insert CR Severity column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append(self.__getPrismContent(importRow[JIRA_CR_ID], SEVERITY))

    def __insertJiraSeverity(self, importRow, exportRow):
        '''
        insert JIRA Severity column.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        exportRow.append([importRow[JIRA_SEVERITY], WHITE_STATUS])

    def __createSheet(self):
        '''
        create a final sheet for writing.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        tempList = []
        for column in self.__exportResultsTitleId:
            tempList.append((column, TITLE_STATUS))

        self.__exportSheet.append(tempList)

        for row in self.__jiraSheet:
            tempSubList = []
            for column in self.__exportResultsTitleId:
                if self.__columnOperator.has_key(column):
                    self.__columnOperator[column](row, tempSubList)
            self.__exportSheet.append(tempSubList)

    def __writeXlsFiles(self):
        '''
        get the xls file content.
        '''
        if DEBUG:
            print "[EXEC] %s.%s" % (self.__class__.__name__, self.__tools.getCurrentFunctionName())

        self.__xlsFile = XlsFile()
        self.__xlsFile.write(self.__exportSheet)

    def exportIssues(self):
        '''
        export all issues.
        '''
        self.__createSheet()
        self.__writeXlsFiles()
