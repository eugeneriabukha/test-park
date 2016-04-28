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
from Utils import *
from Logger import *
import stbt
import time
import collections
import re
import random
import elasticsearch
import cv2

from collections import OrderedDict

# text constants
DEFAULT_SEARCH_CHAR = "P"
SEARCH_NAVIGATION_SUCCESS = "Navigation Success: Search"
SEARCH_NAVIGATION_FAILURE = "Navigation Failure: Search"
POSITIVE_NETFLIX = "The existing setting of Netflix is correct. No further changes"
NEGATIVE_NETFLIX = "The existing Netflix settings is NOT correct. Fixing the search results to incorporate Netflix settings"
INCLUDE_NETFLIX = "Including Netflix"
DIAGNOSTICS = "Diagnostics"
NOT_INCLUDE_NETFLIX = "Not including Netflix"
SEARCH_POSITIVE = "Search performed successfully"
SEARCH_NEGATIVE = "Search Failure: Error in performing search"
POPULAR_SEARCH_RESULTS_MATCH = "The Top 10 most popular search results matches with expected results"
POPULAR_SEARCH_RESULTS_FAILURE = "The most popular search results do not match"
SUMMARYPAGE_TITLE_MATCH = "Correct title is displayed"
SUMMARYPAGE_TITLE_FAILURE = "Incorrect title displayed"
SINGLE_CHAR_SEARCH_RESULTS_MATCH = "Autosuggest with single char search has 4 shows, 2 movies, 2 teams and 1 person"
SINGLE_CHAR_SEARCH_RESULTS_FAILURE = "Autosuggest with single char search has incorrect number of shows/movies/teams/person"
# limit constants
SEARCH_CHAR_UPPER_LIMIT = 30

# list constants
DIAGNOSTICS_KEYSTROKES =[Constants.KEY_EPG,Constants.KEY_MENU,Constants.KEY_DOWN,Constants.KEY_RIGHT,
    Constants.KEY_SELECT,Constants.KEY_DOWN,Constants.KEY_DOWN,Constants.KEY_DOWN,Constants.KEY_SELECT]
HBO_KEYSTROKES = [Constants.KEY_EPG,Constants.KEY_3, Constants.KEY_0, Constants.KEY_0]
GUIDE_NO_DAYS = 7
#SEARCH_KEYSTROKES = [Constants.KEY_EPG,Constants.KEY_MENU,Constants.KEY_DOWN,Constants.KEY_SELECT]
SEARCH_KEYSTROKES = [Constants.KEY_EPG,Constants.KEY_SEARCH]
SEARCH_KEYSTROKES_ADVANCED = [Constants.KEY_RED,Constants.KEY_SELECT]
SEARCH_ADVANCED_OPTIONS = ['Netflix','including','Not','Including']

# General constants
TEXT_TV_SHOW = 'TV Show'
TEXT_MOVIE = 'Movie'
TEXT_GROUP = 'Group'
TEXT_SPORTS = 'Sports'
TEXT_PERSON = 'Person'

TEXT_SUMMARY = 'Summary'
TEXT_EPISODES = 'Episodes'
TEXT_CAST = 'Cast'
TEXT_REVIEWS = 'Reviews'
TEXT_PARENTALGUIDE = 'Parental Guide'
TEXT_TAB_UNAVAILABLE = 'TAB_UNAVAILABLE'

TEXT_STB_MENU = 'MENU'
TEXT_STB_HOME = 'HOME'
TEXT_STB_SHOWS = 'SHOWS'
TEXT_STB_SPORTS = "SPORTS"
TEXT_STB_MOVIES = 'MOVIES'

# Image URL(s)
IMAGE_MENU = '../images/Menu.png'
IMAGE_HOME = '../images/Home.png'
IMAGE_SHOWS = '../images/Shows.png'
IMAGE_SPORTS = '../images/Sports.png'
IMAGE_MOVIES = '../images/Movies.png'

DICT_TOPNAV_IMAGES = { 
    TEXT_STB_MENU : IMAGE_MENU, 
    TEXT_STB_HOME : IMAGE_HOME,
    TEXT_STB_SHOWS : IMAGE_SHOWS,
    TEXT_STB_SPORTS : IMAGE_SPORTS,
    TEXT_STB_MOVIES : IMAGE_MOVIES
    }

# STB Constants
TEXT_STB_MOST_POPULAR_SEARCHES = 'MOST POPULAR SEARCHES'
TEXT_STB_TV = "TV"
TEXT_STB_MOVIE = "MOVIE"
TEXT_STB_PERSON = "PERSON"
TEXT_STB_CHANNEL = "CHANNEL"

DICT_STB_TYPES = {  TEXT_STB_TV : 4,
                    TEXT_STB_MOVIE : 2,
                    TEXT_STB_SPORTS : 2,
                    TEXT_STB_PERSON : 1 }

SEARCH_RESULTS = [TEXT_STB_MOST_POPULAR_SEARCHES,TEXT_STB_TV,TEXT_STB_MOVIE,TEXT_STB_SPORTS,TEXT_STB_PERSON,TEXT_STB_CHANNEL]
SEARCH_RESULTS_EXTENDED = ['MOST','POPULAR','SEARCHES',TEXT_STB_TV,TEXT_STB_MOVIE,TEXT_STB_SPORTS,TEXT_STB_PERSON,TEXT_STB_CHANNEL]
DIAGNOSTICS_LIST = [DIAGNOSTICS]
FRANCHISEPAGE_LIST=['TV','Show','Group','Movie','Sports','Person']
DIAGNOSTICS_LHS = ['Model','Receiver','ID','Smart','Card','Secure','Location','Name','DNASP','Switch',
'Software','Version','Boot','Strap','Available','Joey','Software','Application','Transceiver','Firmware']

# Screen related constants
SCREEN_GUIDE = 'Guide'
SCREEN_SEARCH = 'Search'
SCREEN_DIAGNOSTICS = 'Diagnostics'

# Image related constants
IMAGE_SEARCH = "../images/Search.png"
IMAGE_SUMMARY = "../images/Summary.png"
IMAGE_SUMMARY_SELECTED = "../images/SummarySelected.png"
IMAGE_EPISODES = "../images/Episodes.png"
IMAGE_EPISODES_SELECTED = "../images/EpisodesSelected.png"
IMAGE_CAST = "../images/Cast.png"
IMAGE_CAST_SELECTED = "../images/CastSelected.png"
IMAGE_REVIEWS = "../images/Reviews.png"
IMAGE_PARENTALGUIDE = "../images/ParentalGuide.png"

# Image related lists
IMAGES_SHOW_HEADER = [IMAGE_SUMMARY,IMAGE_EPISODES,IMAGE_CAST]
IMAGES_MOVIE_HEADER = [IMAGE_SUMMARY,IMAGE_CAST]
IMAGES_ACTIVE_SHOW_HEADER = [IMAGE_SUMMARY_SELECTED,IMAGE_EPISODES_SELECTED,IMAGE_CAST_SELECTED,IMAGE_PARENTALGUIDE]
IMAGES_ACTIVE_MOVIE_HEADER = [IMAGE_SUMMARY_SELECTED,IMAGE_CAST_SELECTED,IMAGE_REVIEWS,IMAGE_PARENTALGUIDE]

DICT_FRANCHISE_HEADER_IMAGES = { 
    TEXT_SUMMARY : IMAGE_SUMMARY_SELECTED, 
    TEXT_EPISODES : IMAGE_EPISODES_SELECTED,
    TEXT_CAST : IMAGE_CAST_SELECTED,
    TEXT_REVIEWS : IMAGE_REVIEWS,
    TEXT_PARENTALGUIDE : IMAGE_PARENTALGUIDE
    }

# Region related constants
REGION_NETFLIX = {'x': 1000, 'y': 200, 'width': 500, 'height':600}
REGION_RESULTS = {'x': 472, 'y': 115, 'width': 522, 'height': 590}
REGION_DIAGNOSTICS_LOGO = {'x': 204, 'y': 58, 'width': 154, 'height': 38}
REGION_DIAGNOSTICS = {'x': 270, 'y': 447, 'width': 474, 'height': 41}
REGION_FRANCHISEPAGE = {'x':180,'y': 58, 'width':200, 'height':53}
REGION_PROGRAM_TITLE = {'x':310,'y': 140, 'width':350, 'height':45}
REGION_SPORTS_GROUP_TITLE = {'x':265,'y': 110, 'width':719, 'height':163}
REGION_PERSON_TITLE = {'x':206,'y': 120, 'width':350, 'height':45}
REGION_FRANCHISE_HEADER = {'x':338,'y':42, 'width':648, 'height':69}
REGION_GUIDEPROGRAM = {'x':990,'y':176, 'width':260, 'height':120}
REGION_TOPNAV = {'x':374,'y':44, 'width':626, 'height':76}

DICT_FRANCHISE_TITLE = {
    TEXT_TV_SHOW : REGION_PROGRAM_TITLE,
    TEXT_MOVIE : REGION_PROGRAM_TITLE,
    TEXT_GROUP : REGION_SPORTS_GROUP_TITLE,
    TEXT_SPORTS : REGION_SPORTS_GROUP_TITLE,
    TEXT_PERSON : REGION_PERSON_TITLE,
    }

POSITIONS_MOVIE = { TEXT_SUMMARY:0, TEXT_CAST:1, TEXT_REVIEWS:2, TEXT_PARENTALGUIDE:3 }
POSITIONS_SHOW = { TEXT_SUMMARY:0, TEXT_EPISODES:1, TEXT_CAST:2, TEXT_PARENTALGUIDE:3 }
POSITIONS_TOPNAV = {TEXT_STB_MENU:0,TEXT_STB_HOME:1,TEXT_STB_SHOWS:2,TEXT_STB_SPORTS:3,TEXT_STB_MOVIES:4}

JUNKLIST = ["OQVOU","omfla","'OCDVOU'l4bOD","'OCDVOU'IbOJ","'OCDVOU'IbOJN",'OQVOW<\xa7QNH',"'OGDV0m4bOJNr-'O","OQVOU'IbQN"]

class Navigate:
    """
    Functions required for performing Navigation

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """
    def __init__(self,oInstruction = None):
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
        if oInstruction != None:
            self.instruction = oInstruction

    def Diagnostics(self):
        """
        Navigates to Diagnostics screen.

        Args:
            Nothing

        Returns:
            Nothing

        Raises:
            Nothing
        """
        # press the required key strokes for navigating to diagnostics screen
        Utils.PressListOfKeyStrokes(DIAGNOSTICS_KEYSTROKES)

        # this checks if we are on the right screen, and updates actual result
        bFlag = oDiagnostics.VerifyPage()

        if bFlag == True:
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE

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
        Utils.PressListOfKeyStrokes([Constants.KEY_SEARCH])
        # this checks if we are on the right screen, and updates actual result
        time.sleep(Constants.MEDIUM_WAIT)
        bFlag = oSearch.VerifyPage()
        if bFlag == True:
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE

    def DataDriven(self):
        """
        Navigates to provided screen based on the data provided as direct input

        Args:
            provide list of keystrokes comma seperated and keys should be declared as constants
        """
        oTestData = self.instruction.testdata_detailed
        sDirectInput = oTestData[Constants.DIRECT_INPUT]
        listDirectInput = sDirectInput.split(Constants.DELIMITER_COMMA)
        Logger.note.debug("Direct Input Information:")
        Logger.note.debug(listDirectInput)

        # press the required key strokes for navigating to search screen
        Utils.PressListOfKeyStrokes(listDirectInput)

        # this checks if we are on the right screen, and updates actual result
        time.sleep(Constants.LONG_WAIT)
        self.instruction.actualresult = self.instruction.expectedresult

    def GroupToProgram(self):
        """
        This function navigates the screen from a group page to a movie / tv show

        Args:
            Nothing
            
        Returns:
            Nothing

        Raises:
            Nothing
        """
        Utils.PressListOfKeyStrokes([Constants.KEY_SELECT])
        time.sleep(Constants.LONG_WAIT)

    def Program(self):
        """
        This function navigates within the program - top navigation

        Args:
            sDestinationTabName: In the program top navigation, navigate to the specified tab name
            (default) - Summary
            
        Returns:
            (boolean)

        Raises:
            Nothing
        """

        # fetch data from instruction sheet, else default to summary
        sDirectInput = ""
        bCalledFromInstructionSheet = False
        try:
            oTestData = self.instruction.testdata_detailed
            bCalledFromInstructionSheet = True
            sDirectInput = oTestData[Constants.DIRECT_INPUT]
        except Exception as eError:
            pass

        # if there is a value for direct input, else default it to Summary
        if sDirectInput:
            sDestinationTabName = sDirectInput
        else:
            sDestinationTabName = TEXT_SUMMARY

        # fetch the page name
        sPageName = oFranchisePage.GetPageName()
        listOfImageHeaders = []
        listOfActiveImageHeaders = []

        # update the header list and required variables based on current page
        if(sPageName == TEXT_TV_SHOW):
            listOfImageHeaders = IMAGES_SHOW_HEADER
            listOfActiveImageHeaders = IMAGES_ACTIVE_SHOW_HEADER
            hPositionMap = POSITIONS_SHOW
        elif(sPageName == TEXT_MOVIE):
            listOfImageHeaders = IMAGES_MOVIE_HEADER
            listOfActiveImageHeaders = IMAGES_ACTIVE_MOVIE_HEADER
            hPositionMap = POSITIONS_MOVIE
        else:
            Logger.note.info ("The page do not require any navigation. Page name [%s]" %sPageName)
            if bCalledFromInstructionSheet == True:
                self.instruction.actualresult = self.instruction.expectedresult
            return True

        # Fetch the current tab based on the page
        sCurrentTabName = ""
        sActiveTabName = ""

        # Only show or movie page requires navigation
        sActiveTabName = oFranchisePage.GetCurrentTab(listOfActiveImageHeaders)
        if sActiveTabName == TEXT_TAB_UNAVAILABLE:
            sCurrentTabName = oFranchisePage.GetCurrentTab(listOfImageHeaders)
            # if required tab was not found on all available list of images, then return a false message
            if sCurrentTabName == TEXT_TAB_UNAVAILABLE:
                Logger.note.error( "No matching images available on both active and non active headers. Kindly check the images")
                if bCalledFromInstructionSheet == True:
                    self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
                return False
            else:
                # To navigate in the franchise header, should go all the way up to the header and make it active
                sActiveTabName = sCurrentTabName
                #oImage = DICT_FRANCHISE_HEADER_IMAGES[sActiveTabName]
                #oMatch = stbt.press_until_match(Constants.KEY_UP, oImage, interval_secs=0, max_presses=100, match_parameters=None)
                #if oMatch.match == False:
                #    if bCalledFromInstructionSheet == True:
                #        self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
                #    return False

        # To navigate in the top header, need to find out the current position and work accordingly
        sKeyStroke = Constants.KEY_FRAMEFORWARD
        iCurrentPosition = hPositionMap[sActiveTabName]
        iDestinationPosition = hPositionMap[sDestinationTabName]
        iDifference = iDestinationPosition - iCurrentPosition
        # if the difference is negative, need to move left to reach destination
        if iDifference < 0:
            sKeyStroke = Constants.KEY_FRAMEBACK

        lKeyStrokes = []
        # to decide the number of moves to reach the destination, getting abs of difference
        iLastCounter = abs(iDifference)
        for iCounter in range(0,iLastCounter):
            lKeyStrokes.append(sKeyStroke)
        Utils.PressListOfKeyStrokes(lKeyStrokes)

        # Fetch if the required tab is selected
        sNewTabName = oFranchisePage.GetCurrentTab(listOfActiveImageHeaders)
        if sNewTabName == TEXT_TAB_UNAVAILABLE:
            sNewTabName = oFranchisePage.GetCurrentTab(listOfImageHeaders)

        # check if we reached the tab
        if sNewTabName == sDestinationTabName:
            Logger.note.debug( "Navigation to destination tab [%s] successful" %sDestinationTabName)
            if bCalledFromInstructionSheet == True:
                self.instruction.actualresult = self.instruction.expectedresult
            return True
        else:
            Logger.note.error( "Navigation to destination tab [%s] failure" %sDestinationTabName)
            if bCalledFromInstructionSheet == True:
                self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
            return False

    def TopNav(self):
        """
        This function navigates the top navigation bar

        Args:
            sDestinationTabName: In the program top navigation, navigate to the specified tab name
            (default) - Home
        """
        # fetch data from instruction sheet, else default to summary
        sDirectInput = ""
        bCalledFromInstructionSheet = False
        try:
            oTestData = self.instruction.testdata_detailed
            bCalledFromInstructionSheet = True
            sDirectInput = oTestData[Constants.DIRECT_INPUT]
            sDirectInput = sDirectInput.strip()
            sDirectInput = sDirectInput.upper()
        except Exception as eError:
            pass

        if not sDirectInput:
            if sDirectInput in DICT_TOPNAV_IMAGES:
                Logger.note.debug("User has used a valid navigation scenario: %s" %sDirectInput)
            else:
                Logger.note.error("Please check the provided input for spelling mistakes: %s" %sDirectInput)
                if bCalledFromInstructionSheet == True:
                    self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
                return False

        # if there is a value for direct input, else default it to Menu
        if sDirectInput:
            sDestinationTabName = sDirectInput
        else:
            sDestinationTabName = TEXT_MENU

        # Fetch the current tab based on the page
        sCurrentTabName = ""
        sActiveTabName = ""

        # Fetch the current active tab in the screen
        sActiveTabName = oTopNav.GetCurrentTab()
        if sActiveTabName == TEXT_TAB_UNAVAILABLE:
            Logger.note.error( "Unable to fetch current tab name - Initial Tab")
            if bCalledFromInstructionSheet == True:
                self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
            return False

        # Navigate from current menu to specified tab
        sKeyStroke = Constants.KEY_FRAMEFORWARD
        iCurrentPosition = POSITIONS_TOPNAV[sActiveTabName]
        iDestinationPosition = POSITIONS_TOPNAV[sDestinationTabName]
        iDifference = iDestinationPosition - iCurrentPosition
        # if the difference is negative, need to move left to reach destination
        if iDifference < 0:
            sKeyStroke = Constants.KEY_FRAMEBACK

        lKeyStrokes = []
        # to decide the number of moves to reach the destination, getting abs of difference
        iLastCounter = abs(iDifference)
        for iCounter in range(0,iLastCounter):
            lKeyStrokes.append(sKeyStroke)
        Utils.PressListOfKeyStrokes(lKeyStrokes)

        # Fetch if the required tab is selected
        sNewTabName = oTopNav.GetCurrentTab()
        if sNewTabName == TEXT_TAB_UNAVAILABLE:
            Logger.note.debug( "Unable to verify current tab name - Final Tab")
            if bCalledFromInstructionSheet == True:
                self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
            return False

        # check if we reached the tab
        if sNewTabName == sDestinationTabName:
            Logger.note.debug( "Navigation to destination tab [%s] successful" %sDestinationTabName)
            if bCalledFromInstructionSheet == True:
                self.instruction.actualresult = self.instruction.expectedresult
            return True
        else:
            Logger.note.error( "Navigation to destination tab [%s] failure" %sDestinationTabName)
            if bCalledFromInstructionSheet == True:
                self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
            return False

class Search:
    """
    Functions required for Search like entering Title, verifying results

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """
    def __init__(self,oInstruction = None):
        """
        Initializes the service class with information required for running the test

        Args:
            oInstruction: an instruction object with keyword, its respected expected result,
        option and its data
        """
        if oInstruction != None:
            self.instruction = oInstruction

    def VerifyPage(self):
        """ 
        Updates actual result based on presence of Search image

        Returns:
            Updates actual result based on the current screen details
        """
        bInstructionFlag = False

        try:
            oInstruction = self.instruction
            bInstructionFlag = True
        except Exception as eError:
            pass

        # if the search page do not exist, then exit the test case
        oSearchLogo = stbt.match(IMAGE_SEARCH)
        if oSearchLogo.match == True:
            Logger.note.info( "Navigated to search screen successfully")
            if bInstructionFlag == True:
                self.instruction.actualresult = self.instruction.expectedresult
            else:
                return True
        else:
            Logger.note.error( "Unable to navigate to search screen")
            if bInstructionFlag == True:
                self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
            else:
                return False

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

        if not sTitle:
            self.FetchPopularSearchResults()

        # Random letter or stored values
        if sTitle == Constants.RANDOM_LETTER:
            sTitle = Utils.GetRandomLetter()
        elif sTitle == Constants.STORED:
            sTitle = Utils.GetDynamicTitle()

        # once the title is fetched, get the keystrokes for the title
        lKeyStrokes = EncodeTitle(sTitle,DEFAULT_SEARCH_CHAR)
        Utils.PressListOfKeyStrokes(lKeyStrokes)
        time.sleep(Constants.LONG_WAIT * 2)

        # Performing advanced options
        bActualNetflixStatus = False
        oAdvancedSearchRegion = stbt.Region(x = REGION_NETFLIX['x'], y = REGION_NETFLIX['y'], 
            width = REGION_NETFLIX['width'], height = REGION_NETFLIX['height'])
        textOnScreen = stbt.ocr(region = oAdvancedSearchRegion, tesseract_user_words = SEARCH_ADVANCED_OPTIONS) 
        if(textOnScreen.find(INCLUDE_NETFLIX) != -1):
            bActualNetflixStatus = True

        # Check the current advanced search setting if it matches with the existing setting
        if(bIncludeNetflix == bActualNetflixStatus):
            Logger.note.debug(POSITIVE_NETFLIX)
        else:
            Logger.note.info( NEGATIVE_NETFLIX)
            # performing advanced search : netflix inclusion or removal
            Utils.PressListOfKeyStrokes(SEARCH_KEYSTROKES_ADVANCED)

        # Test after performing advanced search options
        if bIncludeNetflix == True:
            sLookForMessage = INCLUDE_NETFLIX
        else:
            sLookForMessage = NOT_INCLUDE_NETFLIX

        textOnScreen = stbt.ocr(region = oAdvancedSearchRegion, tesseract_user_words = SEARCH_ADVANCED_OPTIONS)
        if textOnScreen.find(sLookForMessage) == -1:
            self.instruction.actualresult = Constants.STATUS_SEARCH_FAILURE
            Logger.note.error( SEARCH_NEGATIVE)
            return
        
        bSucessFlag = self.FetchResults()
        if bSucessFlag == False:
            self.instruction.actualresult = Constants.STATUS_SEARCH_FAILURE
            return

        self.instruction.actualresult = self.instruction.expectedresult
        Logger.note.info(SEARCH_POSITIVE)

    def FetchLastViewed(self):
        """
        Fetches the last watched item only from the screen and adds the details to available variable

        Args:
            Nothing

        Returns:
            Nothing

        Raises:
            Nothing
        """
        # To get more details on the fetched title
        sTitle = Utils.GetDynamicTitle()
        #Logger.note.debug("Current Global Variable: " % SEARCH_RESULTS_EXTENDED)
        #SEARCH_RESULTS_EXTENDED = Utils.ExtendArray(sTitle,SEARCH_RESULTS_EXTENDED)

        # fetch the 0th result region
        sFetchedTitle = Utils.FetchTextOfRegion(REGION_RESULTS,FirstLineOnly=True)
        if sTitle in sFetchedTitle:
            sTitle = sFetchedTitle.split(Constants.DELIMITER_SPACE,1)[1]
            Logger.note.debug("Newly Set Dynamic Title: %s" % sTitle)
            Utils.SetDynamicTitle(sTitle)
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            Logger.note.error('Title on the Guide does not match with Title on Search Results Screen')
            self.instruction.actualresult = Constants.STATUS_FAILURE

    def FetchResults(self):
        """
        Fetches the results on the search screen

        Args:
            Nothing

        Returns:
            Nothing

        Raises:
            Nothing
        """
        Logger.note.debug("Tesseract Keywords: %s" % SEARCH_RESULTS_EXTENDED)

        # fetch the results region
        oResultsRegion = stbt.Region(x = REGION_RESULTS['x'], y = REGION_RESULTS['y'], 
            width = REGION_RESULTS['width'], height = REGION_RESULTS['height'])
        sGivenString = stbt.ocr(region = oResultsRegion, 
            mode = stbt.OcrMode.SINGLE_UNIFORM_BLOCK_OF_TEXT,
            tesseract_user_words = SEARCH_RESULTS_EXTENDED)
        # trimming down unwanted space
        sGivenString = sGivenString.strip()
        # split the different lines captured and strip spaces off each line
        lResults = sGivenString.splitlines()
        lResults = [sLine.strip() for sLine in lResults if sLine.strip()]
        # Remove unrequired junk items
        Logger.note.debug("Provided input for parsing: %s" % lResults)
        for sJunkItem in JUNKLIST:
            if sJunkItem in lResults:
                iIndex = lResults.remove(sJunkItem)
        Logger.note.debug("Input after removing junk list: %s" % lResults)

        # removing numbers prior to text
        for iCounter,sCapturedText in enumerate(lResults):
            try:
                sRegEx = '^[0-9O]\s(.+?)$'
                sFoundText = re.search(sRegEx,sCapturedText).group(1)
                Logger.note.debug("Found Text : %s" % sFoundText)
            except AttributeError:
                sFoundText = sCapturedText
                Logger.note.debug("No matching pattern found for the specified regEx search")
                continue
            lResults[iCounter] = sFoundText

        Logger.note.debug("List after removing numbers prior to text: %s" % lResults)

        # try to check the count for provided title
        sFullURL = Constants.TMS_BASE_URL + ((Constants.INDEX_TMS_MOVIES_PROGRAMS + Constants.DELIMITER_SLASH) * 2)
        sFullURL = sFullURL + Constants.UNDERSCORE_COUNT + Constants.SEARCH_TITLE

        # create a new list for the list to be removed
        listOfJunkItems = []

        # find junk characters from the list captured
        for sCapturedText in lResults:
            try:
                sText = str(sCapturedText)
                sText = sText.replace(Constants.DELIMITER_COLON,"%20") # TODO: need to join the main function
                sText = sText.replace(Constants.DELIMITER_HIFEN,"%20") # TODO: need to join the main function
                sText = sText.replace(Constants.DELIMITER_SLASH,"%20") # TODO: need to join the main function
                sText = sText.replace(Constants.DELIMITER_EXCLAMATION,"%20") # TODO: need to join the main function
                args = {'Title': sText,}
                sURL = sFullURL + '%(Title)s' % args
                Logger.note.debug("URL : %s" % sURL)
                oDetail = Utils.GetHTTPResponse(sURL)
                iTotalSearchCount = oDetail["count"]
                Logger.note.debug("Total Count for %s : %s" % (sText,iTotalSearchCount))
                if iTotalSearchCount == 0:
                    listOfJunkItems.append(sCapturedText)
            except UnicodeEncodeError:
                Logger.note.debug("UnicodeEncodeError for : %s" % sText)
                listOfJunkItems.append(sCapturedText)

        # remove junk characters captured
        for sCapturedText in listOfJunkItems:
            lResults.remove(sCapturedText)
            Logger.note.debug("Removing item from list: %s" % sCapturedText)

        bSucessFlag = self.ParseResults(lResults)
        return bSucessFlag

    def ParseResults(self,lResults):
        """
        Saves the provided result into appropriate data structure in Ultils.py

        Args:
            Takes in String of result set

        Returns:
            Nothing

        Raises:
            Nothing
        """
        # if there is only one result displayed, then its considered none
        if len(lResults) <= 1:
            Logger.note.error("No results displayed on the screen")
            return False

        # Parse the results for most popular searches
        dicIndex = collections.OrderedDict()

        # fetch index of headers
        for sResult in SEARCH_RESULTS:
            try:
                iIndex = lResults.index(sResult)
                dicIndex[sResult] = iIndex
            except Exception as eError:
                continue

        # if there was no known index listed, quit the program
        Logger.note.debug("Index Dictionary : %s" % dicIndex)
        if len(dicIndex) == 0:
            Logger.note.error("No known index to be analyzed. Kindly check the screenshot for more inputs")
            return False

        iMostPopularSearchIndex = -1
        # fetch the first counter based on items in the list
        if TEXT_STB_MOST_POPULAR_SEARCHES in dicIndex:
            iFirstCounter = dicIndex[TEXT_STB_MOST_POPULAR_SEARCHES] + 1
            iMostPopularSearchIndex = dicIndex[TEXT_STB_MOST_POPULAR_SEARCHES]
        else:
            iFirstCounter = dicIndex.values()[0]

        # initialize required variables
        iLastCounter = len(lResults)
        ResultsDict={}
        ListofDict=[]
        sTempType = ""
        iIndexCounter = 1
        if iMostPopularSearchIndex != -1:
            iIndexCounter = iMostPopularSearchIndex
        
        # add items to final dictionary based on its type
        for iCounter in range(iFirstCounter,iLastCounter):
            sCapturedText = str(lResults[iCounter])
            # if valid type is found as one of the item, reset type value and continue
            if sCapturedText in dicIndex:
                sTempType = sCapturedText
                continue

            # add the item into the result dictionary
            ResultsDict["ID"] = iIndexCounter
            # restricting number of characters to an upper limit
            sTempTitle = sCapturedText[0:SEARCH_CHAR_UPPER_LIMIT]
            sTempTitle = str(sTempTitle)
            ResultsDict["Title"] = sTempTitle

            ResultsDict["Type"] = sTempType
            ListofDict.append(ResultsDict.copy())
            iIndexCounter = iIndexCounter + 1

        Logger.note.debug("Parsed result: %s" % ListofDict)

        # Set the Result set under utils
        if len(ListofDict) == 11:
            del ListofDict[-1]

        Logger.note.debug( "Complete List:")
        Logger.note.debug( ListofDict )
        Utils.SetSearchResults(ListofDict)
        return True

    def FetchPopularSearchResults(self):
        """
        Fetches the popular search results from supair

        Args:
            None

        Returns:
            Nothing

        Raises:
            Passes or fails the test based on the comparison
        """
        oPopularSearchResults = Utils.GetHTTPResponse(Constants.POPULAR_SEARCH_URL)
        dicPopularSearch = OrderedDict({})
        for eachPopularSearchItem in oPopularSearchResults:
            iWeight = eachPopularSearchItem["weight"]
            sTMSID = eachPopularSearchItem["tms_id"]
            dicPopularSearch[sTMSID] = iWeight

        sFullURL = Constants.TMS_BASE_URL + ((Constants.INDEX_TMS_MOVIES_PROGRAMS + Constants.DELIMITER_SLASH) * 2)

        dictExpectedResult = OrderedDict({})
        for eachTMSID in dicPopularSearch.keys():
            args = {'TMS_ID': eachTMSID,
                    }
            sURL = sFullURL + '%(TMS_ID)s' % args
            oProgramDetail = Utils.GetHTTPResponse(sURL)
            sTitle = oProgramDetail['_source']['title']
            sTitle = sTitle[0:SEARCH_CHAR_UPPER_LIMIT]
            sTitle = str(sTitle)
            iWeightForTitle = dicPopularSearch[eachTMSID]
            dictExpectedResult[sTitle] = iWeightForTitle

        # save the expected results into utils for future retrieval
        Utils.SetExpectedSearchResults(dictExpectedResult)

        # updated advanced options with collected expected results
        for sTitle in dictExpectedResult.keys():
            #listReturn = Utils.ExtendArray(sTitle)
            #SEARCH_RESULTS_EXTENDED.extend(listReturn)
            sTitle = str(sTitle)
            lTitle = sTitle.split(Constants.DELIMITER_SPACE)
            SEARCH_RESULTS_EXTENDED.extend(lTitle)

        Logger.note.debug("Tesseract Extended: %s" % SEARCH_RESULTS_EXTENDED)

    def VerifyPopularSearchResults(self):
        """
        Verifies the popular search results from supair

        Args:
            None

        Returns:
            Nothing

        Raises:
            Passes or fails the test based on the comparison
        """
        # fetch expected and actual results
        dicExpected = Utils.GetExpectedSearchResults()
        listActual = Utils.GetSearchResults()

        # perform comparison between expected and actual
        bStatus = Utils.CompareResults(dicExpected,listActual)
        if bStatus == True:
            self.instruction.actualresult = self.instruction.expectedresult
            Logger.note.info( POPULAR_SEARCH_RESULTS_MATCH)
        else:

            self.instruction.actualresult = Constants.STATUS_FAILURE
            Logger.note.error( POPULAR_SEARCH_RESULTS_FAILURE)

    def SelectResult(self,iRandID = None):
        """
        Selects one of the popular search result at random

        Args:
            iRandID: if specified, selects specified result. if None, selects a random result
            sType: if specified, selects a random movie/show/sports team/person depending on the type
        Returns:
            Nothing

        Raises:
            Passes or fails the test based on the comparison
        """

        # fetch data from instruction sheet, else default to summary
        sDirectInput = ""
        bCalledFromInstructionSheet = False
        try:
            oTestData = self.instruction.testdata_detailed
            bCalledFromInstructionSheet = True
            sDirectInput = oTestData[Constants.DIRECT_INPUT]
            # capitalize the provided input
            sDirectInput = sDirectInput.upper()
        except Exception as eError:
            pass

        # if there is a value for direct input, else default it to Summary
        if sDirectInput:
            sType = sDirectInput
        else:
            sType = None

        # select the specified title or a random title from the list of programs
        listOfDictSearchResults = Utils.GetSearchResults()

        if sType in DICT_STB_TYPES:
            listOfDictSearchResults = Utils.GetTitleByType(listOfDictSearchResults,sType)
        elif sType == 'DYNAMIC':
            listOfDictSearchResults = Utils.GetTitleByTitle(listOfDictSearchResults,str(Utils.GetDynamicTitle()))

        if len(listOfDictSearchResults) == 0:
            Logger.note.error("The dictionary is empty and cannot be searched")
            self.instruction.actualresult = Constants.STATUS_FAILURE
            return

        Logger.note.debug("Complete List Of Dictionary : %s" % listOfDictSearchResults)
        iLastCounter = len(listOfDictSearchResults) - 1

        if iRandID == None:
            try:
                iRandomID = random.randint(0, iLastCounter)
                Logger.note.debug( "%s from the list is selected at random" % iRandomID)
            except:
                iRandomID = 0

        else:
            iRandomID = iRandID
            Logger.note.info( "User Selected %s from the list" % iRandomID)

        dictSearchItem = listOfDictSearchResults[iRandomID]
        Logger.note.debug(dictSearchItem)
        # fetch the title and save it for future
        sTitle = dictSearchItem["Title"]
        sID = dictSearchItem["ID"]
        Utils.SetSelectedTitle(sTitle)
        Logger.note.info( "Randomly selected title is <%s>" % sTitle)
        # generate the key for the specified program and select the program
        sKey = "KEY_" + str(sID)
        Utils.PressListOfKeyStrokes([sKey])
        time.sleep(Constants.LONG_WAIT * 5)
        self.instruction.actualresult = self.instruction.expectedresult

    def CompareProgramCount(self):
        """
        Compare Program count to verify if there are exact number of movies/shows/teams/person

        Args:
            Nothing

        Returns:
            Nothing

        Raises:
            Passes or fails the test based on the comparison
        """
        
        listOfTypes = DICT_STB_TYPES.keys()
        listOfResults = Utils.GetSearchResults()
        DICT_ACTUAL_TYPE = {}

        for sType in listOfTypes:
            DICT_ACTUAL_TYPE[sType] = len(Utils.GetTitleByType(listOfResults,sType))

        if (DICT_STB_TYPES == DICT_ACTUAL_TYPE):
            Logger.note.info( SINGLE_CHAR_SEARCH_RESULTS_MATCH)
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            Logger.note.error(SINGLE_CHAR_SEARCH_RESULTS_FAILURE)
            for sType in listOfTypes:
                Logger.note.info( "%s : %s" %(sType,DICT_ACTUAL_TYPE[sType]))
            self.instruction.actualresult = Constants.STATUS_FAILURE

class FranchisePage:
    """
    Functions required for the franchise page like Movie, Group, TV Show, Celebrity or a Sports team

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """
    def __init__(self,oInstruction = None):
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
        if oInstruction != None:
            self.instruction = oInstruction

    def GetPageName(self):
        """
        Fetches the page name of the franchise page screen

        Args:
            Nothing

        Returns:
            page name of the displayed page

        Raises:
            Nothing
        """
        sFoundString = Utils.FetchTextOfRegion(REGION_FRANCHISEPAGE,FRANCHISEPAGE_LIST)
        return sFoundString

    def GetCurrentTab(self,listOfImages):
        """
        Fetches the current tab of the franchise page screen

        Args:
            Nothing

        Returns:
            current tab which is selected or which is open

        Raises:
            Nothing
        """
        # Specify the region and check if the image is available in the provided region
        oRegion = Utils.MatchLogo(listOfImages,REGION_FRANCHISE_HEADER)
        sTabName = ""

        # if one of the provided logos was found, return the tab name or provide appropriate negative response
        if oRegion == False:
            sTabName = TEXT_TAB_UNAVAILABLE
        else:
            sTabName = stbt.ocr(region = oRegion)
        return sTabName

    def VerifyProgramTitle(self):
        """
        Verifies if the program title matches with expected

        Args:
            Nothing

        Returns:
            (boolean) based on execution

        Raises:
            Nothing
        """
        sPageName = self.GetPageName()

        # fetch expected title well in hand
        sExpectedTitle = Utils.GetSelectedTitle()
        sExpectedTitle = sExpectedTitle.strip()
        Logger.note.info( "Expected Title: %s" % sExpectedTitle)
        try:
            dicRegion = DICT_FRANCHISE_TITLE[sPageName]
        except:
            Logger.note.error( "Unrecognized page name: %s" % sPageName)
            return False

        # find title from the provided region
        sActualTitle = Utils.FetchTextOfRegion(dicRegion,sExpectedTitle.split(),FirstLineOnly = True)
        sActualTitle = sActualTitle.strip()
        Logger.note.info( "Actual Title: %s" %sActualTitle)
        
        if sActualTitle[0:20].upper() == sExpectedTitle[0:20].upper():
            Logger.note.info(SUMMARYPAGE_TITLE_MATCH)
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            Logger.note.error(SUMMARYPAGE_TITLE_FAILURE)
            self.instruction.actualresult = Constants.STATUS_FAILURE

class Guide:
    """
    Functions required for screen Guide like fetching details from screen

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """
    def __init__(self,oInstruction = None):
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
        if oInstruction != None:
            self.instruction = oInstruction

    def GetPageName(self):
        """
        Fetches the page name of the current screen

        Args:
            Nothing

        Returns:
            page name of the displayed page

        Raises:
            Nothing
        """
        sFoundString = Utils.FetchTextOfRegion(REGION_FRANCHISEPAGE,SCREEN_GUIDE)
        return sFoundString

    def VerifyPage(self):
        """ 
        Updates actual result based on presence of Guide image

        Returns:
            Updates actual result based on the current screen details
        """
        bInstructionFlag = False

        try:
            oInstruction = self.instruction
            bInstructionFlag = True
        except Exception as eError:
            pass

        # if the search page do not exist, then exit the test case
        sTitle = self.GetPageName()
        if sTitle == SCREEN_GUIDE:
            Logger.note.info( "Navigated to Guide page successfully")
            if bInstructionFlag == True:
                self.instruction.actualresult = self.instruction.expectedresult
            else:
                return True
        else:
            Logger.note.error( "Unable to navigate to Guide page")
            if bInstructionFlag == True:
                self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
            else:
                return False

    def NavigateLast(self):
        """ 
        Performs navigation within the guide

        Returns:
            Updates actual result based on the current screen details
        """
        # press key forward for last program
        Utils.PressListOfKeyStrokes([Constants.KEY_FWD] * 9)
        Utils.PressListOfKeyStrokes([Constants.KEY_FRAMEFORWARD] * 11)
        Utils.PressListOfKeyStrokes([Constants.KEY_RIGHT] * 5)
        self.instruction.actualresult = self.instruction.expectedresult

    def MoveAndFetchTitle(self):
        """ 
        Moves forward and fetches a show or movie title

        Returns:
            the fetched title from the screen
        """
        try:
            oTestData = self.instruction.testdata_detailed
            sDirectInput = oTestData[Constants.DIRECT_INPUT]
            if sDirectInput == TEXT_MOVIE:
                for iCounter in range(1,20):
                    sText = Utils.FetchTextOfRegion(REGION_GUIDEPROGRAM)
                    sMovieName = Utils.FetchTextOfRegion(REGION_GUIDEPROGRAM, FirstLineOnly=True)
                    Logger.note.debug("Text on screen: %s" % sText)
                    if TEXT_MOVIE in sText:
                        Utils.SetDynamicTitle(sMovieName[:12])
                        break
                    else:
                        Utils.PressListOfKeyStrokes([Constants.KEY_LEFT])
            elif sDirectInput == TEXT_TV_SHOW:
                # TODO : Still needs to be coded
                Logger.note.error("TV Show functionality still needs to be created")
            self.instruction.actualresult = self.instruction.expectedresult
        except Exception as oException:
            Logger.note.error("Unhandled Exception")
            Logger.note.error(oException)
            self.instruction.actualresult = Constants.STATUS_FAILURE

class Diagnostics:
    """
    Functions required for screen Diagnostics like fetching details from screen

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """
    def __init__(self,oInstruction = None):
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
        if oInstruction != None:
            self.instruction = oInstruction

    def GetPageName(self):
        """
        Fetches the page name of the current page

        Args:
            Nothing

        Returns:
            page name of the displayed page

        Raises:
            Nothing
        """
        sFoundString = Utils.FetchTextOfRegion(REGION_DIAGNOSTICS_LOGO,DIAGNOSTICS_LIST)
        return sFoundString

    def VerifyPage(self):
        """ 
        Updates actual result based on presence of current image

        Returns:
            Updates actual result based on the current screen details
        """
        bInstructionFlag = False
        try:
            oInstruction = self.instruction
            bInstructionFlag = True
        except Exception as eError:
            pass

        # if the search page do not exist, then exit the test case
        sTitle = self.GetPageName()
        if sTitle == SCREEN_DIAGNOSTICS:
            Logger.note.info( "Navigated to Diagnostics page successfully")
            if bInstructionFlag == True:
                self.instruction.actualresult = self.instruction.expectedresult
            else:
                return True
        else:
            Logger.note.error( "Unable to navigate to Diagnostics page")
            if bInstructionFlag == True:
                self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
            else:
                return False

    def FetchDetails(self):
        """
        Fetches & prints the software version from the diagnostics screen

        Args:
            Nothing

        Returns:
            Nothing

        Raises:
            Nothing
        """
        # fetch the text from the results region
        sFoundString = Utils.FetchTextOfRegion(REGION_DIAGNOSTICS)
        Logger.note.info(sFoundString) # Print software version of the stb
        self.instruction.actualresult = self.instruction.expectedresult

class TopNav:
    """
    Functions required for top navigation of the main menu

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """
    def GetCurrentTab(self):
        """
        Fetches the current tab of the top navigator

        Args:
            Nothing

        Returns:
            name of current tab which is selected

        Raises:
            Nothing
        """
        # Specify the region and check if the image is available in the provided region
        listOfImages = DICT_TOPNAV_IMAGES.values()
        oRegion = Utils.MatchLogo(listOfImages,REGION_TOPNAV)
        sTabName = ""

        # if one of the provided logos was found, return the tab name or provide appropriate negative response
        if oRegion == False:
            Logger.note.debug("Tab unavailable at region level")
            sTabName = TEXT_TAB_UNAVAILABLE
        else:
            sTabName = stbt.ocr(region = oRegion)
            sTabName = sTabName.strip()
            sTabName = sTabName.upper()

        if sTabName in DICT_TOPNAV_IMAGES:
            Logger.note.debug("A valid tab found from OCR : %s" %sTabName)
            return sTabName
        else:
            Logger.note.debug("OCR gave an unknown tab name : %s" % sTabName)
            return TEXT_TAB_UNAVAILABLE

# Required variables from the classes on the URL
oNavigate = Navigate()
oFranchisePage = FranchisePage()
oSearch = Search()
oGuide = Guide()
oDiagnostics = Diagnostics()
oTopNav = TopNav()

