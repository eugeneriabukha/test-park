#=============================================================================#
# File: Constants.py
#
#  Copyright (c) 2016, Vinoth Kumar Ravichandran, Prithvi Nath Manikonda
#  All rights reserved.
#
# Description: Holds the constants required for the framework, other utilities
#
# Modules:
#    NA
#
# Classes Added or Extended:
#  N/A
#++
#=============================================================================#

#=============================================================================#
# Class: Constants
#=============================================================================#
#
# Description: Holds the list of constants
#
# Pre-requisites: None
# ++
#=============================================================================#

class Constants(object):
    HELLOA='HEllo'
    #Delimiter(s)
    DELIMITER_UNDERSCORE = "_"
    DELIMITER_SEMICOLON = ";"
    DELIMITER_COLON = ":"
    DELIMITER_EQUAL = "="
    DELIMITER_COMMA = ","
    DELIMITER_HIFEN = "-"
    DELIMITER_STOP = "."

    # Keyword related
    TESTCASE_START = "TestCaseStart"
    TESTCASE_END = "TestCaseEnd"
    TESTCASE = "TestCase"
    SERVICE = "Service"

    # Instruction sheet related
    LABEL = "Label"
    ACTION = "Action"
    TESTDATA = "TestData"
    OPTIONS = "Options"
    EXPECTED_RESULT = "ExpectedResult"
    ACTUAL_RESULT = "ActualResult"
    COMMENTS = "Comments"
    INSTRUCTION = "Instruction"
    DEPENDENCY_FAILURE = "DependencyFailure"
    OPTION_UNDEFINED = "OptionUndefined"
    INSTRUCTIONSHEET_ISSUE = "InstructionSheetIssue"
    DUPLICATE_LABEL = "DuplicateLabel"

    #Status related
    STATUS_SUCCESS = "Success"
    STATUS_FAILURE = "Failure"
    STATUS_NOT_EXECUTED = "NotExecuted"
    #Option related
    COMMENT = "Comment"
    EXIT_ON_ERROR = "ExitOnError"
    EXIT_TC_ON_ERROR = "ExitTCOnError"
    DEPENDS_ON = "DependsOn"
    DIRECT_INPUT = "DirectInput"
    ABOVE = "!ABOVE!"

    # status constants
    STATUS_NAVIGATION_FAILURE = "NavigationFailure"
    STATUS_SEARCH_FAILURE = "SearchFailure"

    # wait related constants
    NO_WAIT = 0
    SHORT_WAIT = 0.5
    MEDIUM_WAIT = 1
    LONG_WAIT = 2

    # List of URL(s)
    POPULAR_SEARCH_URL = "http://tms-catalog-ext.dishanywhere.com:5228/get_popular_search/"

    # Datatable constants
    SEARCH_COL_TITLE = "Title"
    SEARCH_COL_INCLUDE_NETFLIX = "IncludeNetflix"

    CHARACTER_MAP = { 'A':(0,0),'B':(0,1),'C':(0,2),'D':(0,3),'E':(0,4),'F':(0,5),
             'G':(1,0),'H':(1,1),'I':(1,2),'J':(1,3),'K':(1,4),'L':(1,5),
             'M':(2,0),'N':(2,1),'O':(2,2),'P':(2,3),'Q':(2,4),'R':(2,5),
             'S':(3,0),'T':(3,1),'U':(3,2),'V':(3,3),'W':(3,4),'X':(3,5),
             'Y':(4,0),'Z':(4,1),'0':(4,2),'1':(4,3),'2':(4,4),'3':(4,5),
             '4':(5,0),'5':(5,1),'6':(5,2),'7':(5,3),'8':(5,4),'9':(5,5) }
    # Hashes
    OPTIONS_ORDER = { COMMENT : 1, DEPENDS_ON : 2, DIRECT_INPUT : 3, EXIT_ON_ERROR : 4, EXIT_TC_ON_ERROR : 5 }
