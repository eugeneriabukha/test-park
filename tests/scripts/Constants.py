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

    # Hashes
    OPTIONS_ORDER = { COMMENT : 1, DEPENDS_ON : 2, DIRECT_INPUT : 3, EXIT_ON_ERROR : 4, EXIT_TC_ON_ERROR : 5 }
