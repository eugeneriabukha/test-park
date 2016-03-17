"""
.. module:: stb
   :platform: Unix, Windows
   :synopsis: module which holds the classes and functions related to set top box.

.. moduleauthor:: Vinoth Kumar Ravichandran <vinoth.ravichandran@echostar.com>, Prithvi Manikonda <Prithvi.Manikonda@echostar.com>

"""

from KeywordDriver import Instruction
from Constants import Constants
from Encode import EncodeTitle
from Keywords import *
import stbt
import time

# COMMON CONSTANTS
DEFAULT_SEARCH_CHAR = "P"
SEARCH_NAVIGATION_SUCCESS = "Navigation Success: Search"
SEARCH_NAVIGATION_FAILURE = "Navigation Failure: Search"
SEARCH_CORRECT_NETFLIX_SETTING = "The existing setting of Netflix is correct. No further changes"
SEARCH_KEYSTROKES = ['KEY_EPG','KEY_MENU','KEY_DOWN','KEY_SELECT']
SEARCH_KEYSTROKES_ADVANCED = ['KEY_RED','KEY_SELECT']
SEARCH_ADVANCED_OPTIONS = ['Netflix','including','Not','Including']
IMAGE_SEARCH_LOGO = "../images/Search_Logo.png"
POSITIVE_NETFLIX = "The existing setting of Netflix is correct. No further changes"
NEGATIVE_NETFLIX = "The existing Netflix settings is NOT correct. Fixing the search results to incorporate Netflix settings"
INCLUDE_NETFLIX = "Including Netflix"
NOT_INCLUDE_NETFLIX = "Not including Netflix"
SEARCH_POSITIVE = "Search performed successfully"
SEARCH_NEGATIVE = "Search Failure: Error in performing search"
REGION_ADVANCED_SEARCH = {'x': 1000, 'y': 200, 'width': 500, 'height':600};

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

# public instantition of the cCommon class to be used by other Classes
Common = cCommon()

class Navigate:
    """
    Functions required for performing Navigation

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """
    def __init__(self,oInstruction):
        """
        Initializes the service class with information required for running the test

        Args:
            oInstruction: an instruction object with keyword, its respected expected result,
            option and its data

        Returns:
            Nothing

        Raises:
            Nothing
        """
        self.instruction = oInstruction

    def Search(self):
        """
        Navigates to search screen. Updates actual result based on presence of Search image

        Args:
            Nothing

        Returns:
            Nothing

        Raises:
            Nothing
        """
        # press the required key strokes for navigating to search screen
        Common.PressListOfKeyStrokes(SEARCH_KEYSTROKES)

        # this checks if we are on the right screen, and updates actual result
        time.sleep(Constants.LONG_WAIT)
        oSearchLogo = stbt.match(IMAGE_SEARCH_LOGO)

        # if the search page do not exist, then exit the test case
        if oSearchLogo.match == True:
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE

class Search:
    """
    Functions required for Search like entering Title, verifying results

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """

    def __init__(self,oInstruction):
        """
        Initializes the service class with information required for running the test

        Args:
            oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

        Returns:
            Nothing

        Raises:
            Nothing
        """
        self.instruction = oInstruction

    def Title(self):
        """
        Enters the provided title in the testdata_detailed in the Instruction object while initialize

        Args:
            Nothing

        Returns:
            Nothing

        Raises:
            Nothing
        """
        global global_wait

        # fetch data from the instruction
        oTestData = self.instruction.testdata_detailed
        for dValue in oTestData.values():
            sTitle = dValue[Constants.SEARCH_COL_TITLE]
            bIncludeNetflix = dValue[Constants.SEARCH_COL_INCLUDE_NETFLIX]

        # once the title is fetched, get the keystrokes for the title
        lKeyStrokes = EncodeTitle(sTitle,DEFAULT_SEARCH_CHAR)
        Common.PressListOfKeyStrokes(lKeyStrokes)

        # Performing advanced options
        bActualNetflixStatus = False
        oAdvancedSearchRegion = stbt.Region(x = REGION_ADVANCED_SEARCH['x'], y = REGION_ADVANCED_SEARCH['y'], width = REGION_ADVANCED_SEARCH['width'], height = REGION_ADVANCED_SEARCH['height'])
        textOnScreen = stbt.ocr(region = oAdvancedSearchRegion, tesseract_user_words = SEARCH_ADVANCED_OPTIONS) 
        if(textOnScreen.find(INCLUDE_NETFLIX) != -1):
            bActualNetflixStatus = True

        # Check the current advanced search setting if it matches with the existing setting
        if(bIncludeNetflix == bActualNetflixStatus):
            print POSITIVE_NETFLIX
        else:
            print NEGATIVE_NETFLIX
            # performing advanced search : netflix inclusion or removal
            Common.PressListOfKeyStrokes(SEARCH_KEYSTROKES_ADVANCED)

        # Test after performing advanced search options
        if bIncludeNetflix == True:
            sLookForMessage = INCLUDE_NETFLIX
        else:
            sLookForMessage = NOT_INCLUDE_NETFLIX

        textOnScreen = stbt.ocr(region = oAdvancedSearchRegion, tesseract_user_words = SEARCH_ADVANCED_OPTIONS)
        if textOnScreen.find(sLookForMessage) != -1:
            self.instruction.actualresult = self.instruction.expectedresult
            print SEARCH_POSITIVE
        else:
            self.instruction.actualresult = Constants.STATUS_SEARCH_FAILURE
            print SEARCH_NEGATIVE

        #resultsRegion = stbt.Region(x = 400, y = 100, width = 600, height = 700)

#=============================================================================#
# End Of Class: stb
#=============================================================================#
