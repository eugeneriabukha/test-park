from KeywordDriver import Instruction
from Constants import Constants
from Encode import EncodeTitle
from Keywords import *
import stbt
import time

#=============================================================================#
# File: stb.py
#
#  Copyright (c) 2015, Vinoth Kumar Ravichandran, Prithvi Nath Manikonda
#  All rights reserved.
#
# Description: Classes and functions for set top box
#    These classes and functions are application dependent, performs activities based
#    on the user input from the instruction sheet
#
#    The keyword passed on from instruction sheet is analyzed and appropriate
#    class and its methods would be dynamically called based on instruction
#
#--
# Depends On:
#    KeywordDriver
#    Encode
#    Constants
#
#++
#=============================================================================#

# COMMON CONSTANTS
DEFAULT_SEARCH_CHAR = 'P'

#=============================================================================#
# Class: Navigate
#
# Description: Functions for class Navigate
#    These functions and methods are platform dependent
#
#  Key:   () = No parameters,  (...) = parameters required
#
# Methods:
#   __init__(oInstruction)
#   ()
#
# Pre-requisites:
# ++
#=============================================================================#
class Navigate:
    #=============================================================================#
    # Method: initialize()
    # Description: Initializes the service class with information required for running the test
    # Returns: NA
    # Usage Examples: STB.new(oInstruction)
    # where oInstruction should be of class Instruction
    #=============================================================================#
    def __init__(self,oInstruction):
        self.instruction = oInstruction

    #=============================================================================#
    # Method: Search
    # Description:
    # Returns: NA
    # Usage Examples:
    #=============================================================================#
    def Search(self):
        # press search button
        stbt.press('KEY_EPG')
        # press menu button
        stbt.press('KEY_MENU')
        stbt.press('KEY_DOWN')
        # get down to select search
        stbt.press('KEY_SELECT')

        # this checks if we are on the right screen, and updates actual result
        oResults = stbt.match_text("Search")
        if oResults.match == True:
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE

        print oResults.region

#=============================================================================#
# Class: Search
#
# Description: Functions for class Search
#    These functions and methods are platform dependent
#
#  Key:   () = No parameters,  (...) = parameters required
#
# Methods:
#   __init__(oInstruction)
#   EnterTitle()
#
# Pre-requisites:
# ++
#=============================================================================#
class Search:
    #=============================================================================#
    # Method: initialize()
    # Description: Initializes the service class with information required for running the test
    # Returns: NA
    # Usage Examples: STB.new(oInstruction)
    # where oInstruction should be of class Instruction
    #=============================================================================#
    def __init__(self,oInstruction):
        self.instruction = oInstruction

    #=============================================================================#
    # Method:
    # Description:
    # Returns: NA
    # Usage Examples:
    #=============================================================================#
    def Title(self):
        global global_wait

        # check for presence of Search Logo
        oSearchLogo = stbt.match("../images/Search_Logo.png")

        # fetch data from the instruction
        oTestData = self.instruction.testdata_detailed
        for dValue in oTestData.values():
            sTitle = dValue[Constants.SEARCH_COL_TITLE]
            bIncludeNetflix = dValue[Constants.SEARCH_COL_INCLUDE_NETFLIX]

        # once the title is fetched, get the keystrokes for the title
        lKeyStrokes = EncodeTitle(sTitle,DEFAULT_SEARCH_CHAR)
        # run the key strokes on the set top box
        for keyStroke in lKeyStrokes:
            stbt.press(keyStroke)
            time.sleep(global_wait)

        # TODO: to get output information about the current netflix level and set it in the flag bFlag
        # TODO: make use of the variables
        #a = stbt.Region(800,100,width=500,height=500)
        #oResults = stbt.match_text("Net",None,a,4)
        # print stbt.ocr(None,stbt.Region.ALL,1)
        # print "+++++++"
        # print stbt.ocr(None,stbt.Region.ALL,6)
        # print "+++++++"
        # print stbt.ocr(None,stbt.Region.ALL,3)
        # print "+++++++"
        # print stbt.ocr(None,stbt.Region.ALL,4)
        # print "+++++++"
        # print stbt.ocr(None,stbt.Region.ALL,5)
        #print stbt.match("../data/Search_Logo.png",None,stbt.MatchParameters(None, 0.5))
        
        stbt.match("../images/Search_NoNetflix.png")
        stbt.match("../images/Search_Netflix.png")


        bFlag = True

        # netflix would be set to run when bFlag information is false
        if bFlag == False:
            stbt.press('KEY_RED')
            time.sleep(Constants.SHORT_WAIT)
            stbt.press('KEY_SELECT')
            time.sleep(Constants.SHORT_WAIT)



#=============================================================================#
# End Of Class: stb
#=============================================================================#
