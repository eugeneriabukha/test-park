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
import stbt
import time
import collections
import re
import random
import elasticsearch
from collections import OrderedDict

# text constants
DEFAULT_SEARCH_CHAR = "P"
SEARCH_NAVIGATION_SUCCESS = "Navigation Success: Search"
SEARCH_NAVIGATION_FAILURE = "Navigation Failure: Search"
SEARCH_CORRECT_NETFLIX_SETTING = "The existing setting of Netflix is correct. No further changes"
POSITIVE_NETFLIX = "The existing setting of Netflix is correct. No further changes"
NEGATIVE_NETFLIX = "The existing Netflix settings is NOT correct. Fixing the search results to incorporate Netflix settings"
INCLUDE_NETFLIX = "Including Netflix"
DIAGNOSTICS = "Diagnostics"
NOT_INCLUDE_NETFLIX = "Not including Netflix"
SEARCH_POSITIVE = "Search performed successfully"
SEARCH_NEGATIVE = "Search Failure: Error in performing search"
POPULAR_SEARCH_RESULTS_MATCH = "The Top 10 most popular search results matches with expected results"
POPULAR_SEARCH_RESULTS_FAILURE = "The most popular search results do not match"
SUMMARYPAGE_TITLE_MATCH = "Correct Show or Movie is displayed"
SUMMARYPAGE_TITLE_FAILURE = "Incorrect Show or Movie is displayed"

# limit constants
SEARCH_CHAR_UPPER_LIMIT = 30

# list constants
DIAGNOSTICS_KEYSTROKES=[Constants.KEY_EPG,Constants.KEY_MENU,Constants.KEY_DOWN,Constants.KEY_RIGHT,
    Constants.KEY_SELECT,Constants.KEY_DOWN,Constants.KEY_DOWN,Constants.KEY_DOWN,Constants.KEY_SELECT]
SEARCH_KEYSTROKES = [Constants.KEY_EPG,Constants.KEY_MENU,Constants.KEY_DOWN,Constants.KEY_SELECT]
SEARCH_KEYSTROKES_ADVANCED = [Constants.KEY_RED,Constants.KEY_SELECT]
SEARCH_ADVANCED_OPTIONS = ['Netflix','including','Not','Including']
SEARCH_RESULTS = ['MOST POPULAR SEARCHES','TV','MOVIE','SPORTS','PERSON','CHANNEL']
SEARCH_RESULTS_EXTENDED = ['MOST','POPULAR','SEARCHES','TV','MOVIE','SPORTS','PERSON','CHANNEL']
DIAGNOSTICS_LIST = [DIAGNOSTICS]
FRANCHISEPAGE_LIST=['TV','Show','Group','Movie','Sports','Person']
DIAGNOSTICS_LHS = ['Model','Receiver','ID','Smart','Card','Secure','Location','Name','DNASP','Switch',
'Software','Version','Boot','Strap','Available','Joey','Software','Application','Transceiver','Firmware']

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
REGION_RESULTS = {'x': 490, 'y': 123, 'width': 475, 'height': 590}
REGION_DIAGNOSTICS_LOGO = {'x': 204, 'y': 58, 'width': 154, 'height': 38}
REGION_DIAGNOSTICS = {'x': 270, 'y': 447, 'width': 474, 'height': 41}
REGION_FRANCHISEPAGE = {'x':180,'y': 58, 'width':200, 'height':53}
REGION_PROGRAM_TITLE = {'x':310,'y': 140, 'width':350, 'height':45}
REGION_SPORTS_GROUP_TITLE = {'x':286,'y': 120, 'width':350, 'height':45}
REGION_PERSON_TITLE = {'x':206,'y': 120, 'width':350, 'height':45}
REGION_FRANCHISE_HEADER = {'x':338,'y':42, 'width':648, 'height':69}

DICT_FRANCHISE_TITLE = {
    TEXT_TV_SHOW : REGION_PROGRAM_TITLE,
    TEXT_MOVIE : REGION_PROGRAM_TITLE,
    TEXT_GROUP : REGION_SPORTS_GROUP_TITLE,
    TEXT_SPORTS : REGION_SPORTS_GROUP_TITLE,
    TEXT_PERSON : REGION_PERSON_TITLE,
    }

class Navigate:
    """
    Functions required for performing Navigation

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """
    def __init__(self,oInstruction=None):
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
        if oInstruction !=None:
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
        sFoundString = Utils.FetchTextOfRegion(REGION_DIAGNOSTICS_LOGO,DIAGNOSTICS_LIST)
        bDiagnostics = False
        if(sFoundString.find(DIAGNOSTICS) != -1):
            bDiagnostics = True

        # if the search page do not exist, then exit the test case
        if bDiagnostics == True:
            print "Navigated to Diagnostics screen successfully"
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            print "Unable to navigate to Diagnostics screen"
            self.instruction.actualresult = Constants.STATUS_FAILURE


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
        Utils.PressListOfKeyStrokes(SEARCH_KEYSTROKES)

        # this checks if we are on the right screen, and updates actual result
        time.sleep(Constants.LONG_WAIT)
        oSearchLogo = stbt.match(IMAGE_SEARCH)

        # if the search page do not exist, then exit the test case
        if oSearchLogo.match == True:
            print "Navigated to Search screen successfully"
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            print "Unable to navigate to Diagnostics screen"
            self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE

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
            sDirectInput = oTestData[Constants.DIRECT_INPUT]
            bCalledFromInstructionSheet = True
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
            hPositionMap = Constants.SHOW_POSITIONS
        elif(sPageName == TEXT_MOVIE):
            listOfImageHeaders = IMAGES_MOVIE_HEADER
            listOfActiveImageHeaders = IMAGES_ACTIVE_MOVIE_HEADER
            hPositionMap = Constants.MOVIE_POSITIONS
        else:
            print "The page do not require any navigation. Page name [%s]" %sPageName
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
                print "No matching images available on both active and non active headers. Kindly check the images"
                if bCalledFromInstructionSheet == True:
                    self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
                return False
            else:
                # To navigate in the franchise header, should go all the way up to the header and make it active
                sActiveTabName = sCurrentTabName
                oImage = DICT_FRANCHISE_HEADER_IMAGES[sActiveTabName]
                oMatch = stbt.press_until_match(Constants.KEY_UP, oImage, interval_secs=0, max_presses=100, match_parameters=None)
                if oMatch.match == False:
                    if bCalledFromInstructionSheet == True:
                        self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
                    return False

        # To navigate in the top header, need to find out the current position and work accordingly
        sKeyStroke = Constants.KEY_RIGHT
        iCurrentPosition = hPositionMap[sActiveTabName]
        iDestinationPosition = hPositionMap[sDestinationTabName]
        iDifference = iDestinationPosition - iCurrentPosition
        # if the difference is negative, need to move left to reach destination
        if iDifference < 0:
            sKeyStroke = Constants.KEY_LEFT

        lKeyStrokes = []
        # to decide the number of moves to reach the destination, getting abs of difference
        iLastCounter = abs(iDifference)
        for iCounter in range(0,iLastCounter):
            lKeyStrokes.append(sKeyStroke)
        Utils.PressListOfKeyStrokes(lKeyStrokes)

        # Fetch if the required tab is selected
        sNewTabName = oFranchisePage.GetCurrentTab(listOfActiveImageHeaders)
        if sNewTabName == sDestinationTabName:
            print "Navigation to destination tab [%s] successful" %sDestinationTabName
            if bCalledFromInstructionSheet == True:
                self.instruction.actualresult = self.instruction.expectedresult
            return True
        else:
            print "Navigation to destination tab [%s] failure" %sDestinationTabName
            if bCalledFromInstructionSheet == True:
                self.instruction.actualresult = Constants.STATUS_NAVIGATION_FAILURE
            return False

'''
    def TopNav(self,textOnScreen):
        """
        This function navigates the screen to summary page based on the present screen

        Args:
            textOnScreen (String):  String which tells which screen the stb is at present
            
        Returns:
            (boolean):  Sucess or Failure to navigate to summary page

        Raises:
            Nothing
        """
        #if(textOnScreen == GROUP):
        #    Utils.PressListOfKeyStrokes([Constants.KEY_SELECT])
        #    time.sleep(Constants.LONG_WAIT)

        if(textOnScreen == TEXT_TV_SHOW):
            oMatchResult = stbt.press_until_match(Constants.KEY_UP, IMAGE_EPISODES_SELECTED, interval_secs=0, max_presses=100, match_parameters=None)  
            if oMatchResult.match == True:
                #Constants.OnTopNav = True
                Utils.PressListOfKeyStrokes([Constants.KEY_LEFT])
                time.sleep(Constants.LONG_WAIT)  
                #Constants.PRESENT_TAB = TEXT_SUMMARY
                return True 
            else:
                print "Cannot Navigate to Summary Page"
                #Constants.OnTopNav = False
                return False
        else:
            time.sleep(Constants.LONG_WAIT)
            oMatchResult = stbt.press_until_match(Constants.KEY_UP, IMAGE_SUMMARY_SELECTED, interval_secs=0, max_presses=100, match_parameters=None)
            if oMatchResult.match == True:
                #Constants.OnTopNav = True
                #Constants.PRESENT_TAB = TEXT_SUMMARY
                return True
            else:
                print "Cannot Navigate to Summary Page"
                #Constants.OnTopNav = False
                return False

    def Programs(self,textOnScreen,sDestinationTab):
        """
        This function navigates the screen to summary page based on the present screen

        Args:
            textOnScreen (String):  String which tells which screen the stb is at present
            sSelectedTab(String) : Present Tab that is selected
            sDestinationTab(String): Final tab to be navigated to
        Returns:
            (boolean):  Sucess or Failure to navigate to summary page

        Raises:
            Nothing
        """
        # if the user is already on the top nav, perform navigation on the top nav
        #if Constants.OnTopNav == True:
        lKeyStrokes = []
        iDiff = 0
        sKeyStroke = KEY_RIGHT
        if textOnScreen == TEXT_TV_SHOW:
            iDiff = Constants.SHOW_TAB_MAP[sDestinationTab]-Constants.SHOW_TAB_MAP[Constants.PRESENT_TAB]
        elif textOnScreen == TEXT_MOVIE:
            iDiff=Constants.SHOW_TAB_MAP[sDestinationTab]-Constants.MOVIE_TAB_MAP[Constants.PRESENT_TAB]
        if iDiff < 0:
            sKeyStroke = Constants.KEY_LEFT

        # Get list of keystrokes to an list to move to the destination object
        for iCounter in range(0,abs(iDiff)):
            lKeyStrokes.append(sKeyStroke)

        Utils.PressListOfKeyStrokes(lKeyStrokes)
        Constants.PRESENT_TAB = sDestinationTab
        #else:
        #    print "The focus is not in the top nav, hence navigation would not be performed"
'''

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

        self.FetchPopularSearchResults()
        # fetch data from the instruction
        oTestData = self.instruction.testdata_detailed
        for dValue in oTestData.values():
            sTitle = dValue[Constants.SEARCH_COL_TITLE]
            bIncludeNetflix = dValue[Constants.SEARCH_COL_INCLUDE_NETFLIX]

        # once the title is fetched, get the keystrokes for the title
        lKeyStrokes = EncodeTitle(sTitle,DEFAULT_SEARCH_CHAR)
        Utils.PressListOfKeyStrokes(lKeyStrokes)

        # Performing advanced options
        bActualNetflixStatus = False
        oAdvancedSearchRegion = stbt.Region(x = REGION_NETFLIX['x'], y = REGION_NETFLIX['y'], 
            width = REGION_NETFLIX['width'], height = REGION_NETFLIX['height'])
        textOnScreen = stbt.ocr(region = oAdvancedSearchRegion, tesseract_user_words = SEARCH_ADVANCED_OPTIONS) 
        if(textOnScreen.find(INCLUDE_NETFLIX) != -1):
            bActualNetflixStatus = True

        # Check the current advanced search setting if it matches with the existing setting
        if(bIncludeNetflix == bActualNetflixStatus):
            print POSITIVE_NETFLIX
        else:
            print NEGATIVE_NETFLIX
            # performing advanced search : netflix inclusion or removal
            Utils.PressListOfKeyStrokes(SEARCH_KEYSTROKES_ADVANCED)

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
        self.FetchResults()

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
        # fetch the results region
        oResultsRegion = stbt.Region(x = REGION_RESULTS['x'], y = REGION_RESULTS['y'], 
            width = REGION_RESULTS['width'], height = REGION_RESULTS['height'])
        sGivenString = stbt.ocr(region = oResultsRegion, tesseract_user_words = SEARCH_RESULTS_EXTENDED)
        # trimming down unwanted space
        sGivenString = sGivenString.strip()
        # split the different lines captured and strip spaces off each line
        lResults = sGivenString.splitlines()
        lResults = [sLine.strip() for sLine in lResults if sLine.strip()]
        self.ParseResults(lResults)

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
        # Parse the results for most popular searches
        dicIndex = collections.OrderedDict()
        
        # fetch index of headers
        for sResult in SEARCH_RESULTS:
            try:
                iIndex = lResults.index(sResult)
                dicIndex[sResult] = iIndex
            except Exception as eError:
                continue
        ResultsDict={}
        ListofDict=[]
        sTempType = ""

        if lResults[0] == SEARCH_RESULTS[0]:
            lResults.remove(SEARCH_RESULTS[0])
            sTempType = Constants.EMPTY
            # Keeps the counter for the ID in the search results
            iIndexCounter = 0
            for sCurrentLine in lResults:
                # Searches for the pattern match of any string that starts with number and followed by space
                if re.search('^[0-9O]\s', sCurrentLine) != None:
                    #Gets the index and title by spliting the Current line
                    sIndex = sCurrentLine.split(' ',1)[0]
                    sTitle = sCurrentLine.split(' ',1)[1]
                    ResultsDict["ID"] = iIndexCounter
                    ResultsDict["Title"] = sTitle[0:SEARCH_CHAR_UPPER_LIMIT]
                    ResultsDict["Type"] = sTempType
                    # Appending the results dict into the list
                    ListofDict.append(ResultsDict.copy())
                    iIndexCounter = iIndexCounter + 1
                # Searches the pattern which starts with any alphanumber char followed by anything that is not space
                elif re.search('^[a-zA-Z0-9]\S', sCurrentLine) != None:
                    ResultsDict["ID"] = iIndexCounter
                    ResultsDict["Title"] = sCurrentLine[0:SEARCH_CHAR_UPPER_LIMIT]
                    ResultsDict["Type"] = sTempType
                    ListofDict.append(ResultsDict.copy())
                    iIndexCounter = iIndexCounter + 1
                # Ignoring any other read on the search which is not alphanumeric
                else:
                    pass
        # Parse the results when a search is made
        else:
            # Get the length of the Result string
            iLastCounter = len(lResults)
            iIndexCounter = 1
            for iCounter in range(1, iLastCounter):
                sCurrentLine = lResults[iCounter]
                if sCurrentLine in dicIndex:
                    sTempType = sCurrentLine
                else:
                    sIndex = iIndexCounter
                    #Gets the title by spliting the Current line
                    if sCurrentLine.strip(" ") == "":
                        continue
                    try:
                        sTitle = sCurrentLine.split(' ',1)[1]
                        ResultsDict["ID"] = sIndex
                        sTempTitle = sTitle[0:SEARCH_CHAR_UPPER_LIMIT]
                        sTempTitle = str(sTempTitle)
                        ResultsDict["Title"] = sTempTitle
                        ResultsDict["Type"] = sTempType
                        # Appending the results dict into the list
                        ListofDict.append(ResultsDict.copy())
                        # incrementing the Index Counter which keeps track of the ID
                        iIndexCounter = iIndexCounter + 1
                    except:
                        pass

        # Set the Result set under utils
        if len(ListofDict) == 11:
            del ListofDict[-1]

        Utils.SetSearchResults(ListofDict)

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
            sTitle = str(sTitle)
            lTitle = sTitle.split(" ")
            SEARCH_RESULTS_EXTENDED.extend(lTitle)

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
            print POPULAR_SEARCH_RESULTS_MATCH
        else:
            self.instruction.actualresult = Constants.STATUS_FAILURE
            print POPULAR_SEARCH_RESULTS_FAILURE

    def SelectResult(self,iRandID = None):
        """
        Selects one of the popular search result at random

        Args:
            iRandID: if specified, selects specified result. if None, selects a random result

        Returns:
            Nothing

        Raises:
            Passes or fails the test based on the comparison
        """
        # select the specified title or a random title from the list of programs
        listOfDictSearchResults = Utils.GetSearchResults()
        iLastCounter = len(listOfDictSearchResults) - 1


        if iRandID == None:
            try:
                iRandomID = random.randint(0, iLastCounter)
                print "%s from the list is selected at random" %iRandomID
            except:
                iRandomID = 0
        else:
            iRandomID = iRandID
            print "User Selected the %s from the list" %iRandomID


        dictSearchItem = listOfDictSearchResults[iRandomID]

        # fetch the title and save it for future
        sTitle = dictSearchItem["Title"]
        sID = dictSearchItem["ID"]
        Utils.SetSelectedTitle(sTitle)
        print "The Selected Title is %s" %sTitle
        # generate the key for the specified program and select the program
        sKey = "KEY_" + str(sID)
        Utils.PressListOfKeyStrokes([sKey])
        time.sleep(Constants.LONG_WAIT * 2)

    def Letter(self,cLetter=None):
        """
        Selects one of the popular search result at random

        Args:
            cLetter: if specified, searches of specified letter. if None, searches a char at random

        Returns:
            Nothing

        Raises:
            Passes or fails the test based on the comparison
        """
        if cLetter==None:
            cRandChar=Utils.GetRandomLetter()
        else:
            cRandChar=cLetter

        lKeyStrokes = EncodeTitle(cRandChar,DEFAULT_SEARCH_CHAR)
        Utils.PressListOfKeyStrokes(lKeyStrokes)

        self.FetchResults()
        print Utils.GetSearchResults()



        # this checks if we are on the right screen, and updates actual result
        #oFranchiseRegion = stbt.Region(x = REGION_FRANCHISEPAGE['x'], y = REGION_FRANCHISEPAGE['y'], 
        #    width = REGION_FRANCHISEPAGE['width'], height = REGION_FRANCHISEPAGE['height'])
        #sTextOnScreen = stbt.ocr(region = oFranchiseRegion, tesseract_user_words = FRANCHISEPAGE_LIST) 
        #sTextOnScreen = sTextOnScreen.strip()
        #oNavigate.TopNav(sTextOnScreen)

        #sTitleOnScreen = Utils.FetchTextOfRegion(REGION_TITLE,sTitle.split())
        #sTitleOnScreen = sTitleOnScreen[0:SEARCH_CHAR_UPPER_LIMIT]
        #if sTitle == sTitleOnScreen:
        #    print "Program Title matches for the selected title"
        #else:
        #    print "Program Title do not match for the selected title. Expected %s | Actual %s" %(sTitle,sTitleOnScreen)

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
        print "Expected Title: %s" %sExpectedTitle
        try:
            dicRegion = DICT_FRANCHISE_TITLE[sPageName]
        except:
            print "Unrecognized page name: %s" %sPageName
            return False

        # find title from the provided region
        sActualTitle = Utils.FetchTextOfRegion(dicRegion,sExpectedTitle.split())
        print "Actual Title: %s" %sActualTitle
        if sActualTitle[0:20] ==sExpectedTitle[0:20]:
            print SUMMARYPAGE_TITLE_MATCH
        else:
            print SUMMARYPAGE_TITLE_FAILURE



class Diagnostics:
    """
    Functions required for screen Diagnostics like fetching details from screen

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
        print sFoundString # Print software version of the stb
        self.instruction.actualresult = self.instruction.expectedresult

# Required variables from the classes on the URL
oNavigate = Navigate()
oFranchisePage = FranchisePage()
