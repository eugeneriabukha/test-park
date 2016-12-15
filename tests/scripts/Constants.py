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
    #Delimiter(s)
    DELIMITER_UNDERSCORE = "_"
    DELIMITER_SEMICOLON = ";"
    DELIMITER_COLON = ":"
    DELIMITER_EQUAL = "="
    DELIMITER_COMMA = ","
    DELIMITER_HIFEN = "-"
    DELIMITER_STOP = "."
    DELIMITER_SLASH = "/"
    DELIMITER_SPACE = " "
    DELIMITER_PIPE = "|"
    DELIMITER_EXCLAMATION = "!"
    DELIMITER_OPENBRACE = "("
    DELIMITER_CLOSEBRACE = ")"
    DEILIMITER_STAR = "*"
    DELIMITER_SINGLE_QUOTE = "'"
    DELIMITER_AMBERSENT = "&"

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
    EXPECTED_MESSAGE = "ExpectedMessage"
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
    STATUS_SKIPPED = "Skipped"

    #Option related
    COMMENT = "Comment"
    EXIT_ON_ERROR = "ExitOnError"
    EXIT_TC_ON_ERROR = "ExitTCOnError"
    DEPENDS_ON = "DependsOn"
    DIRECT_INPUT = "DirectInput"
    ABOVE = "!ABOVE!"
    EMPTY = "!EMPTY!"
    RANDOM_LETTER = "!RANDOM_LETTER!"
    STORED = "!STORED!"
    NETFLIX = "!NETFLIX!"
    DYNAMIC = "DYNAMIC"
    SEARCHED = "!SEARCHED!"

    # status constants
    STATUS_NAVIGATION_FAILURE = "NavigationFailure"
    STATUS_SEARCH_FAILURE = "SearchFailure"

    # wait related constants
    NO_WAIT = 0
    SHORT_WAIT = 0.5
    MEDIUM_WAIT = 1
    LONG_WAIT = 2

    # Key related constants
    KEY_0 = "KEY_0"
    KEY_1 = "KEY_1"
    KEY_2 = "KEY_2"
    KEY_3 = "KEY_3"
    KEY_4 = "KEY_4"
    KEY_5 = "KEY_5"
    KEY_6 = "KEY_6"
    KEY_7 = "KEY_7"
    KEY_8 = "KEY_8"
    KEY_9 = "KEY_9"
    KEY_CANCEL = "KEY_CANCEL"
    KEY_DOWN = "KEY_DOWN"
    KEY_EPG = "KEY_EPG"
    KEY_FRAMEBACK = "KEY_FRAMEBACK"
    KEY_FRAMEFORWARD = "KEY_FRAMEFORWARD"
    KEY_FWD = "KEY_FWD"
    KEY_INFO = "KEY_INFO"
    KEY_LAST = "KEY_LAST"
    KEY_LEFT = "KEY_LEFT"
    KEY_MENU = "KEY_MENU"
    KEY_NUMERIC_POUND = "KEY_NUMERIC_POUND"
    KEY_NUMERIC_STAR = "KEY_NUMERIC_STAR"
    KEY_PAUSE = "KEY_PAUSE"
    KEY_RED = "KEY_RED"
    KEY_RIGHT = "KEY_RIGHT"
    KEY_SEARCH = "KEY_SEARCH"
    KEY_SELECT = "KEY_SELECT"
    KEY_TV = "KEY_TV"
    KEY_UP = "KEY_UP"
    KEY_PAGEDOWN = "KEY_PAGEDOWN"
    KEY_PAGEUP = "KEY_PAGEUP"

    # List of URL(s)
    POPULAR_SEARCH_URL = "http://aws-qa-supair-admin.metacloud.media/get_popular_search/"
    #TMS_BASE_URL = "http://tms-catalog.dishanywhere.com:9200/"
    TMS_BASE_URL = "http://chy-prod-supair-admin.metacloud.media:9200/"
    NETFLIX_ORIGINALS_URL = "http://aws-qa-supair-admin.metacloud.media/api_netflix_originals_list/"

    # List of index(es)
    INDEX_TMS_MOVIES_PROGRAMS = "tms_movies_programs"
    UNDERSCORE_COUNT = "_count"
    SEARCH_TITLE = "?q=title:"

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
