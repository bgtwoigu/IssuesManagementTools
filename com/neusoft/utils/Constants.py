#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on Aug 25, 2015

@author: liuzhsh
'''

DEBUG = False

class FoundException(Exception): pass

CREATED_ID_FILE = "./Configuration/created_id.csv"
ET_OR_BY_CASE_ID_FILE = "./Configuration/et_or_by_case.csv"
EXPORT_RESULTS_TITLE_ID_FILE = "./Configuration/export_results_title_id.csv"
JIRA_STATUS_ID_FILE = "./Configuration/jira_status_id.csv"
MODULE_ID_FILE = "./Configuration/module_id.csv"
PL_STATUS_ID_FILE = "./Configuration/pl_status_id.csv"
PRODUCT_ID_FILE = "./Configuration/product_id.csv"
REPORTER_ID_FILE = "./Configuration/reporter_id.csv"
REPRODUCED_ID_FILE = "./Configuration/reproduced_id.csv"
TEAM_ID_FILE = "./Configuration/team_id.csv"

JIRA_SOURCES_FILE = "./Sources/SearchRequest-73122.xls"
PRISM_SOURCES_FILE = "./Sources/PrismSearchResults.csv"

RESULTS_FILE = "./Results/ExportResults.xls"

XLS_SHEET_INDEX = 0
ZERO = 0

KEY = 0
VALUE = 1

CONTENT = 0
STATUS = 1

JIRA_ISSUE_TYPE = "Issue Type"
JIRA_KEY = "Key"
JIRA_SUMMARY = "Summary"
JIRA_ASSIGNEE = "Assignee"
JIRA_REPORTER = "Reporter"
JIRA_STATUS = "Status"
JIRA_CREATED = "Created"
JIRA_UPDATED = "Updated"
JIRA_RCA = "RCA"
JIRA_CR_ID = "CRID"
JIRA_ISSUE_CLOSE_REASON = "Issue Close Reason"
JIRA_COMPONENTS = "Component/s"
JIRA_ISSUE_PRIORITY_IN_PRISM = "Issue Priority in Prism"
JIRA_SEVERITY = "Severity"
JIRA_DESCRIPTION = "Description"

TITLE_STATUS = "T"
CHANGE_STATUS = "C"
ERROR_STATUS = "E"
WHITE_STATUS = "W"
HIGHLIGHT_STATUS = "H"

PL_STATUS = "PLStatus"
CR_ASSIGNEE_USER_NAME = "CRAssigneeUserName"
SUB_SYSTEM = "Subsystem"
TAG_NAMES = "TagNames"
TEST_CASE_NUMBER = "TestCaseNumber"
SEVERITY = "Severity"
CR_PRIORITY = "CRPriority"

ERROR = "ERROR"
BLANK = ""

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

EMPTY_TYPE = 0
TEXT_TYEP = 1
NUMBER_TYPE = 2
DATE_TYPE = 3
BOOLEAN_TYPE = 4
ERROR_TYPE = 5
BLANK_TYPE = 6
