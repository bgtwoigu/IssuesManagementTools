#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on Aug 25, 2015

@author: liuzhsh
'''

DEBUG = False

class FoundException(Exception): pass

ZERO = 0

TEAM_ID_FILE = "./Configuration/team_id.csv"
MODULE_ID_FILE = "./Configuration/module_id.csv"
ET_OR_BY_CASE_ID_FILE = "./Configuration/et_or_by_case.csv"
REPORTER_ID_FILE = "./Configuration/reporter_id.csv"
PRODUCT_ID_FILE = "./Configuration/product_id.csv"
REPRODUCED_ID_FILE = "./Configuration/reproduced_id.csv"
CREATED_ID_FILE = "./Configuration/created_id.csv"
JIRA_STATUS_ID_FILE = "./Configuration/jira_status_id.csv"
PL_STATUS_ID_FILE = "./Configuration/pl_status_id.csv"
JIRA_SOURCES_FILE = "./Sources/SearchRequest-73122.xls"
PRISM_SOURCES_FILE = "./Sources/PrismSearchResults.csv"
RESULTS_FILE = "./Results/ExportResults.xls"

KEY = 0
VALUE = 1

DELETE_COLUMN_NUM = 1

EXPORT_SHEET_TITLE = ["Issue Type", "Key", "Summary", "Assignee", "Reporter", "JIRA Status", "Created", "Updated", "RCA", "CRID", "Issue Close Reason", "Subsystem", "Team", "Module", "ET/by case", "Reporter", "Product", "PL Status", "Reproduced on 8952", "TagNames", "TestCaseNumber"]

COLUMN_SUM = 21

ERROR = "ERROR"
BLANK = ""

CHANGE_STATUS = "C"
ERROR_STATUS = "E"
BLACK_STATUS = "B"
HIGHLIGHT_STATUS = "H"

SUMMARY_COLUMN_NO = 2
ASSIGNEE_COLUMN_NO = 3
REPORTER_1_COLUMN_NO = 4
JIRA_STATUS_COLUMN_NO = 5
CREATED_TIME_COLUMN_NO = 6
UPDATED_TIME_COLUMN_NO = 7
CR_ID_COLUMN_NO = 9
COMPONENTS_COLUMN_NO = 11
TEAM_COLUMN_NO = 12
MODULE_COLUMN_NO = 13
ET_OR_BY_CASE_COLUMN_NO = 14
REPORTER_2_COLUMN_NO = 15
PRODUCT_COLUMN_NO = 16
PL_STATUS_COLUMN_NO = 17
REPRODUCED_COLUMN_NO = 18
TAG_NAMES_COLUMN_NO = 19
TEST_CASE_NUMBER_COLUMN_NO = 20

PRISM_PL_STATUS_COLUMN_NO = 1

PL_STATUS = "PLStatus"
CR_ASSIGNEE_USER_NAME = "CRAssigneeUserName"
SUB_SYSTEM = "Subsystem"
TAG_NAMES = "TagNames"
TEST_CASE_NUMBER = "TestCaseNumber"

TEST_CASE_NUMBER_IDENTIFIER = "EXPLORATORY_TESTING"
TAG_NAMES_IDENTIFIER = ("MON", "POT")

YEAR = 0
MONTH = 1
DAY = 2
HOUR = 3
MINUTE = 4
SECOND = 5
TIME_DICT = {'BEGIN' : ('1900', '01', '01', '00', '00', '00'), 'END': ('2900', '12', '31', '23', '59', '59')}

JIRA_OPEN_STATUS = "Open"

BEGIN_TIME = "BEGIN"
END_TIME = "END"
