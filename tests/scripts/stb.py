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
DEFAULT_SEARCH_CHAR = "P"
SEARCH_NAVIGATION_SUCCESS = "Navigation Success: Search"
SEARCH_NAVIGATION_FAILURE = "Navigation Failure: Search"
SEARCH_CORRECT_NETFLIX_SETTING = "The existing setting of Netflix is correct. No further changes"
SEARCH_KEYSTROKES = ['KEY_EPG','KEY_MENU','KEY_DOWN','KEY_SELECT']
IMAGE_SEARCH_LOGO = "../images/Search_Logo.png"


class cCommon:
    """
    We use this as a common class to hold all common functions.

    .. note::
       A public object is instantiated which can be used by all other classes 

    """
    def PressListOfKeyStrokes(self,lListOfKeyStrokes):
        """
        This function performs the list of key strokes provided on the parameter

        Args:
            lListOfKeyStrokes (list):  list of valid keystrokes

        Returns:
            Nothing

        Raises:
            Nothing

        """
        global global_wait

        # press keystrokes for search
        for sKeyStroke in lListOfKeyStrokes:
            stbt.press(sKeyStroke)
            time.sleep(global_wait)

Common = cCommon
"""
public instantition of the cCommon class to be used by other Classes
"""

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
        global Common

        Common.PressListOfKeyStrokes(SEARCH_KEYSTROKES)

        # this checks if we are on the right screen, and updates actual result
        time.sleep(Constants.LONG_WAIT)
        oSearchLogo = stbt.match(IMAGE_SEARCH_LOGO)

        # if the search page do not exist, then exit the test case
        if oSearchLogo.match == True:
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE

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
#   Title()
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
    def getResults(self):
            resultsRegion = stbt.Region(x=400, y=100, width=600, height=700)
            resultsString = stbt.ocr(region=resultsRegion, tesseract_user_words=['MOVIE','TV','SPORTS','PERSON','0']) 
            resultsString = resultsString.strip()
            resultsString = list(resultsString)
            resultsString[0] = '0'
            resultsString = ''.join(resultsString)
            resultsString =resultsString.splitlines()
            resultsString = [line.strip() for line in resultsString if line.strip()]
            indexTV = -1
            indexMovie = -1
            indexSports = -1
            indexPeople = -1
            if 'TV' in resultsString:
                indexTV = resultsString.index('TV')
            if 'MOVIE' in resultsString:
                indexMovie = resultsString.index('MOVIE')
            if 'SPORTS' in resultsString:
                indexSports = resultsString.index('SPORTS')
            if 'PERSON' in resultsString:
                indexPeople = resultsString.index('PERSON')
            listResults = resultsString[:1]
            listTV = []
            listMovie = []
            listPeople = []
            listSports = []
            if(indexTV != -1):
                if(indexMovie != -1):
                    listTV = resultsString[indexTV+1:indexMovie]
                elif(indexSports != -1):
                    listTV = resultsString[indexTV+1:indexSports]
                elif(indexPeople != -1):
                    listTV = resultsString[indexTV+1:indexPeople]
                else:
                    listTV = resultsString[indexTV+1:]
            if(indexMovie != -1):
                if(indexSports != -1):
                    listMovie = resultsString[indexMovie+1:indexSports]
                elif(indexPeople != -1):
                    listMovie = resultsString[indexMovie+1:indexPeople]
                else:
                    listMovie = resultsString[indexMovie+1:]
            if(indexSports != -1):
                if(indexPeople != -1):
                    listSports = resultsString[indexSports+1:indexPeople]
                else:
                    listSports = resultsString[indexSports+1:]
            if(indexPeople != -1):
                listPeople = resultsString[indexPeople+1:]

            self.ResultMatrix = []
            dictResults = {'Firstline':listResults,'TV':listTV,'Movie':listMovie,'Person':listPeople,'Sports':listSports}
            for key in dictResults.keys():
                for value in dictResults[key]:
                    index = value.split(' ',1)[0]
                    title = value.split(' ',1)[1]
                    self.ResultMatrix.append((key,index,title))
            time.sleep(Constants.LONG_WAIT)
            return self.ResultMatrix

    #=============================================================================#
    # Method:
    # Description:
    # Returns: NA
    # Usage Examples:
    #=============================================================================#
    def SearchResultbyIndex(self,index):  
        return [item for item in self.ResultMatrix if item[1] == index]     

    #=============================================================================#
    # Method:
    # Description:
    # Returns: NA
    # Usage Examples:
    #=============================================================================#
    def SearchResultsbyType(self,typevideo):
        return [item for item in self.ResultMatrix if item[0] == typevideo]

    #=============================================================================#
    # Method:
    # Description:
    # Returns: NA
    # Usage Examples:
    #=============================================================================#
    def SearchResultsbyTitle(self,title):
        return [item for item in self.ResultMatrix if item[2] == title]

    #=============================================================================#
    # Method:
    # Description:
    # Returns: NA
    # Usage Examples:
    #=============================================================================#
    def Title(self):
        global global_wait
        global Common
        
        # fetch data from the instruction
        oTestData = self.instruction.testdata_detailed
        for dValue in oTestData.values():
            sTitle = dValue[Constants.SEARCH_COL_TITLE]
            bIncludeNetflix = dValue[Constants.SEARCH_COL_INCLUDE_NETFLIX]

        # once the title is fetched, get the keystrokes for the title
        lKeyStrokes = EncodeTitle(sTitle,DEFAULT_SEARCH_CHAR)
        Common.PressListOfKeyStrokes(SEARCH_KEYSTROKES)

        # run the key strokes on the set top box
        #for keyStroke in lKeyStrokes:
        #    stbt.press(keyStroke)
        #    time.sleep(global_wait)
        
        # Needed a short wait before capturing the details from the screen
        time.sleep(Constants.SHORT_WAIT)

        bActualNetflixStatus = False
        textOnScreen = stbt.ocr(region=stbt.Region(x=1000, y=200, width=500, height=600), tesseract_user_words=['Netflix','including','Not','Including']) 
        if(textOnScreen.find("Including Netflix") != -1):
            bActualNetflixStatus = True

        if(bIncludeNetflix == bActualNetflixStatus):
            print "The existing setting of Netflix is correct. No further changes"
        else:
            print "The existing Netflix settings is NOT correct. Fixing the search results to incorporate Netflix settings"
            # fixing netflix results
            stbt.press('KEY_RED')
            time.sleep(Constants.SHORT_WAIT)
            stbt.press('KEY_SELECT')
            time.sleep(Constants.LONG_WAIT)

        resultsRegion = stbt.Region(x=400, y=100, width=600, height=700)
        #print stbt.ocr(region=resultsRegion, tesseract_user_words=['MOVIE','TV','SPORTS','PERSON','0']) 
        print self.getResults()
        time.sleep(Constants.LONG_WAIT)

        # 
        if bIncludeNetflix == True:
            sLookForMessage = "Including Netflix"
        else:
            sLookForMessage = "Not including Netflix"

        textOnScreen = stbt.ocr(region=stbt.Region(x=1000, y=200, width=500, height=600), tesseract_user_words=['Netflix','including','Not','Including']) 
        if textOnScreen.find(sLookForMessage) != -1:
            self.instruction.actualresult = self.instruction.expectedresult
            print "Search performed successfully"
        else:
            self.instruction.actualresult = Constants.STATUS_SEARCH_FAILURE
            print "Search Failure: Error in performing search"


#=============================================================================#
# End Of Class: stb
#=============================================================================#
