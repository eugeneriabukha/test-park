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
        # check for presence of Search Logo
        time.sleep(Constants.LONG_WAIT)
        oSearchLogo = stbt.match("../images/Search_Logo.png")

        # if the search page do not exist, then exit the test case
        if oSearchLogo.match == True:
            self.instruction.actualresult = self.instruction.expectedresult
            print "Navigation To Search Screen: Successful"
        else:
            self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
            print "Navigation Failure: Unable to navigate to Search screen"

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
        
        # Fetch the current status for netflix results
        if bIncludeNetflix == True:
            sImagePath = "../images/Search_Netflix.png"
        else:
            sImagePath = "../images/Search_NoNetflix.png"

        # Check for presence of netflix
        bCurrentNetflixStatus = stbt.match(sImagePath).match
        if bCurrentNetflixStatus == True:
            print "The existing setting of Netflix is correct. No further changes"
        else:
            print "The existing Netflix settings is NOT correct. Fixing the search results to incorporate Netflix settings"
            # fixing netflix results
            stbt.press('KEY_RED')
            time.sleep(Constants.SHORT_WAIT)
            stbt.press('KEY_SELECT')

        # Check status after fixing Netflix results
        bCurrentNetflixStatus = stbt.match(sImagePath).match
        if bCurrentNetflixStatus == True:
            self.instruction.actualresult = self.instruction.expectedresult
            print "Search performed successfully"
        else:
            self.instruction.actualresult = Constants.STATUS_SEARCH_FAILURE
            print "Search Failure: Error in performing search"

        #stbt.match("../images/Search_NoNetflix.png")
        #stbt.match("../images/Search_Netflix.png")







#=============================================================================#
# End Of Class: stb
#=============================================================================#
