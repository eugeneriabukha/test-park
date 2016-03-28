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

# limit constants
SEARCH_CHAR_UPPER_LIMIT = 30

# list constants
DIAGNOSTICS_KEYSTROKES=['KEY_EPG','KEY_MENU','KEY_DOWN','KEY_RIGHT','KEY_SELECT','KEY_DOWN','KEY_DOWN','KEY_DOWN','KEY_SELECT']
SEARCH_KEYSTROKES = ['KEY_EPG','KEY_MENU','KEY_DOWN','KEY_SELECT']
SEARCH_KEYSTROKES_ADVANCED = ['KEY_RED','KEY_SELECT']
SEARCH_ADVANCED_OPTIONS = ['Netflix','including','Not','Including']
SEARCH_RESULTS = ['MOST POPULAR SEARCHES','TV','MOVIE','SPORTS','PERSON','CHANNEL']
SEARCH_RESULTS_EXTENDED = ['MOST','POPULAR','SEARCHES','TV','MOVIE','SPORTS','PERSON','CHANNEL']
DIAGNOSTICS_LIST = [DIAGNOSTICS]
FRANCHISEPAGE_LIST=['TV','Show','Group','Movie']
DIAGNOSTICS_LHS = ['Model','Receiver','ID','Smart','Card','Secure','Location','Name','DNASP','Switch',
'Software','Version','Boot','Strap','Available','Joey','Software','Application','Transceiver','Firmware']

# Image related
IMAGE_SEARCH_LOGO = "../images/Search_Logo.png"
IMAGE_EPISODES_SELECTED="../images/EpisodesSelected.png"
IMAGE_SUMMARY_SELECTED="../images/SummarySelected.png"

# Region related
REGION_NETFLIX = {'x': 1000, 'y': 200, 'width': 500, 'height':600}
REGION_RESULTS = {'x': 490, 'y': 123, 'width': 475, 'height': 590}
REGION_DIAGNOSTICS_LOGO = {'x': 204, 'y': 58, 'width': 154, 'height': 38}
#REGION_DIAGNOSTICS = {'x': 237, 'y': 132, 'width': 516, 'height': 522}
REGION_DIAGNOSTICS = {'x': 270, 'y': 447, 'width': 474, 'height': 41}
REGION_FRANCHISEPAGE={'x':180,'y': 58, 'width':230, 'height':53}
REGION_TITLE={'x':286,'y': 112, 'width':468, 'height':72}

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
        oDiagnosticsRegion = stbt.Region(x = REGION_DIAGNOSTICS_LOGO['x'], y = REGION_DIAGNOSTICS_LOGO['y'], 
            width = REGION_DIAGNOSTICS_LOGO['width'], height = REGION_DIAGNOSTICS_LOGO['height'])
        textOnScreen = stbt.ocr(region = oDiagnosticsRegion, tesseract_user_words = DIAGNOSTICS_LIST) 

        bDiagnostics = False
        if(textOnScreen.find(DIAGNOSTICS) != -1):
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
        oSearchLogo = stbt.match(IMAGE_SEARCH_LOGO)

        # if the search page do not exist, then exit the test case
        if oSearchLogo.match == True:
            print "Navigated to Search screen successfully"
            self.instruction.actualresult = self.instruction.expectedresult
        else:
            print "Unable to navigate to Diagnostics screen"
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
                    # Striping the .. Characters that show up if the result is too long
                    #ResultsDict["Title"] = sTitle.strip(".")
                    ResultsDict["Title"] = sTitle[0:SEARCH_CHAR_UPPER_LIMIT]
                    ResultsDict["Type"] = sTempType
                    # Appending the results dict into the list
                    ListofDict.append(ResultsDict.copy())
                    iIndexCounter = iIndexCounter + 1
                # Searches the pattern which starts with any alphanumber char followed by anything that is not space
                elif re.search('^[a-zA-Z0-9]\S', sCurrentLine) != None:
                    ResultsDict["ID"] = iIndexCounter
                    #ResultsDict["Title"] = sCurrentLine.strip(".")
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
            iIndexCounter = 0
            for iCounter in range(1, iLastCounter):
                sCurrentLine = lResults[iCounter]
                if sCurrentLine in dicIndex:
                    sTempType = sCurrentLine
                else:
                    sIndex = iIndexCounter
                    #Gets the title by spliting the Current line
                    if sCurrentLine.strip(" ") == "":
                        continue
                    sTitle = sCurrentLine.split(' ',1)[1]
                    ResultsDict["ID"] = sIndex
                    # Striping the .. Characters that show up if the result is too long
                    #ResultsDict["Title"] = sTitle.strip(".")
                    ResultsDict["Title"] = sTitle[0:SEARCH_CHAR_UPPER_LIMIT]
                    ResultsDict["Type"] = sTempType
                    # Appending the results dict into the list
                    ListofDict.append(ResultsDict.copy())
                    # incrementing the Index Counter which keeps track of the ID
                    iIndexCounter = iIndexCounter + 1
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

        if(textOnScreen=='Group'):
            Utils.PressListOfKeyStrokes(["KEY_SELECT"])
            time.sleep(Constants.LONG_WAIT)  

        if(textOnScreen=='TV Show'):
            matchresult=stbt.press_until_match("KEY_UP", IMAGE_EPISODES_SELECTED, interval_secs=0, max_presses=100, match_parameters=None)  
            if matchresult.match==True:
                Constants.OnTopNav=True
                self.PressListOfKeyStrokes(['KEY_LEFT'])
                time.sleep(Constants.LONG_WAIT)  
                Constants.PRESENT_TAB='Summary'
                return True 
            else:
                print "Cannot Navigate to Summary Page"
                Constants.OnTopNav=False
                return False
        else:
            time.sleep(Constants.LONG_WAIT)  
            matchresult=stbt.press_until_match("KEY_UP", IMAGE_SUMMARY_SELECTED, interval_secs=0, max_presses=100, match_parameters=None)
            Constants.OnTopNav=True
            Constants.PRESENT_TAB='Summary'
            return True

    def NavBarPrograms(self,textOnScreen,sSelectedTab,sDestinationTab):
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
        lKeyStrokes=[]
        if textOnScreen=='TV Show':
            diff=Constants.SHOW_TAB_MAP[sDestinationTab]-Constants.SHOW_TAB_MAP[sSelectedTab];
            if diff<0:
                for i in range(0,abs(diff)):
                    lKeyStrokes.append('KEY_LEFT')
            else:
                for i in range(0,abs(diff)):
                    lKeyStrokes.append('KEY_RIGHT')
            Utils.PressListOfKeyStrokes(lKeyStrokes)
            Constants.OnTopNav=True
            Constants.PRESENT_TAB=sDestinationTab
        if textOnScreen=='MOVIE':
            diff=Constants.SHOW_TAB_MAP[sDestinationTab]-Constants.MOVIE_TAB_MAP[sSelectedTab];
            if diff<0:
                for i in range(0,abs(diff)):
                    lKeyStrokes.append('KEY_LEFT')
            else:
                for i in range(0,abs(diff)):
                    lKeyStrokes.append('KEY_RIGHT')
            Utils.PressListOfKeyStrokes(lKeyStrokes)
            Constants.OnTopNav=True
            Constants.PRESENT_TAB=sDestinationTab

    def SelectRandomResult(self,RandID=None):
        """
        Selects one of the popular search result at random

        Args:
            None

        Returns:
            Nothing

        Raises:
            Passes or fails the test based on the comparison
        """
        if RandID==None:
            iRandID=random.randint(0, 9)
        else:
            iRandID=RandID

        sTitle=Utils.GetTitleByID(Utils.GetSearchResults(),iRandID)[0]['Title']

        sKey="KEY_"+str(iRandID)

        Utils.PressListOfKeyStrokes([sKey])
        time.sleep(Constants.LONG_WAIT*2)
        # this checks if we are on the right screen, and updates actual result
        oFranchiseRegion = stbt.Region(x = REGION_FRANCHISEPAGE['x'], y = REGION_FRANCHISEPAGE['y'], 
            width = REGION_FRANCHISEPAGE['width'], height = REGION_FRANCHISEPAGE['height'])
        textOnScreen = stbt.ocr(region = oFranchiseRegion, tesseract_user_words = FRANCHISEPAGE_LIST) 
        textOnScreen=textOnScreen.strip()


        oTitleRegion=stbt.Region(x = REGION_TITLE['x'], y = REGION_TITLE['y'], 
            width = REGION_TITLE['width'], height = REGION_TITLE['height'])

        self.TopNav(textOnScreen)
        sTitleOnScreen = stbt.ocr(region = oTitleRegion, tesseract_user_words = sTitle.split()) 
        sTitleOnScreen=sTitleOnScreen[0:SEARCH_CHAR_UPPER_LIMIT]
        if sTitle==sTitleOnScreen:
            print "Success!!!!!Hurray"
        else:
            print ":( :( "

    

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
        # fetch the results region
        oDiagnosticsRegion = stbt.Region(x = REGION_DIAGNOSTICS['x'], y = REGION_DIAGNOSTICS['y'], 
            width = REGION_DIAGNOSTICS['width'], height = REGION_DIAGNOSTICS['height'])
        sExtractedString = stbt.ocr(region = oDiagnosticsRegion)

        # Print software version of the stb
        print sExtractedString
        self.instruction.actualresult = self.instruction.expectedresult

