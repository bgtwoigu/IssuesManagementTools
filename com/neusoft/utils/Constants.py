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
JIRA_SOURCES_FILE = "./Sources/SearchRequest-73122.xls"
PRISM_SOURCES_FILE = "./Sources/PrismSearchResults.csv"
RESULTS_FILE = "./Results/ExportResults.xls"

KEY = 0
VALUE = 1

DELETE_COLUMN_NUM = 1

ADDITIONAL_TITLE = ["Team", "Module", "ET/by case", "Reporter", "Product", "PL Status", "Reproduced on 8952", "Modify"]

COLUMN_SUM = 20

ERROR = "ERROR"
BLANK = ""

CHANGE_STATUS = "C"
ERROR_STATUS = "E"

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

PL_STATUS = "PLStatus"
CR_ASSIGNEE_USER_NAME = "CRAssigneeUserName"
SUB_SYSTEM = "Subsystem"