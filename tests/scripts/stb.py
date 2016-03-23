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
NOT_INCLUDE_NETFLIX = "Not including Netflix"
SEARCH_POSITIVE = "Search performed successfully"
SEARCH_NEGATIVE = "Search Failure: Error in performing search"

# list constants
SEARCH_KEYSTROKES = ['KEY_EPG','KEY_MENU','KEY_DOWN','KEY_SELECT']
SEARCH_KEYSTROKES_ADVANCED = ['KEY_RED','KEY_SELECT']
SEARCH_ADVANCED_OPTIONS = ['Netflix','including','Not','Including']
SEARCH_RESULTS = ['MOST POPULAR SEARCHES','TV','MOVIE','SPORTS','PERSON','CHANNEL']

# Image related
IMAGE_SEARCH_LOGO = "../images/Search_Logo.png"

# Region related
REGION_NETFLIX = {'x': 1000, 'y': 200, 'width': 500, 'height':600}
REGION_RESULTS = {'x': 395, 'y': 100, 'width': 600, 'height': 700}


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
        Utils.PressListOfKeyStrokes(SEARCH_KEYSTROKES)

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
        Utils.PressListOfKeyStrokes(lKeyStrokes)

        # Performing advanced options
        bActualNetflixStatus = False
        oAdvancedSearchRegion = stbt.Region(x = REGION_NETFLIX['x'], y = REGION_NETFLIX['y'], width = REGION_NETFLIX['width'], height = REGION_NETFLIX['height'])
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
        oResultsRegion = stbt.Region(x = REGION_RESULTS['x'], y = REGION_RESULTS['y'], width = REGION_RESULTS['width'], height = REGION_RESULTS['height'])
        sGivenString = stbt.ocr(region = oResultsRegion, tesseract_user_words = SEARCH_RESULTS)
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
            sTempType=' '
            # Keeps the counter for the ID in the search results
            iIndexCounter=0
            for sCurrentLine in lResults:
                # Searches for the pattern match of any string that starts with number and followed by space
                if re.search('^[0-9O]\s', sCurrentLine) !=None:
                    #Gets the index and title by spliting the Current line
                    sIndex=sCurrentLine.split(' ',1)[0]
                    sTitle=sCurrentLine.split(' ',1)[1]
                    ResultsDict["ID"]=iIndexCounter
                    # Striping the .. Characters that show up if the result is too long
                    ResultsDict["Title"]=sTitle.strip(".")
                    ResultsDict["Type"]=sTempType
                    # Appending the results dict into the list
                    ListofDict.append(ResultsDict.copy())
                    iIndexCounter=iIndexCounter+1
                # Searches the pattern which starts with any alphanumber char followed by anything that is not space
                elif re.search('^[a-zA-Z0-9]\S', sCurrentLine) !=None:
                    ResultsDict["ID"]=iIndexCounter
                    ResultsDict["Title"]=sCurrentLine.strip(".")
                    ResultsDict["Type"]=sTempType
                    ListofDict.append(ResultsDict.copy())
                    iIndexCounter=iIndexCounter+1
                # Ignoring any other read on the search which is not alphanumeric
                else:
                    pass
        # Parse the results when a search is made
        else:
            # Get the length of the Result string
            iLastCounter = len(lResults)
            iIndexCounter=0
            for iCounter in range(1, iLastCounter):
                sCurrentLine = lResults[iCounter]
                if sCurrentLine in dicIndex:
                    sTempType = sCurrentLine
                else:
                    sIndex=iIndexCounter
                    #Gets the title by spliting the Current line
                    sTitle=sCurrentLine.split(' ',1)[1]
                    ResultsDict["ID"]=sIndex
                    # Striping the .. Characters that show up if the result is too long
                    ResultsDict["Title"]=sTitle.strip(".")
                    ResultsDict["Type"]=sTempType
                    # Appending the results dict into the list
                    ListofDict.append(ResultsDict.copy())
                    # incrementing the Index Counter which keeps track of the ID
                    iIndexCounter=iIndexCounter+1
        # Set the Result set under utils
        Utils.SetSearchResults(ListofDict)

    def VerifyPopularSearchResults(self):
        """
        Fetches the popular search results from supair and compares it with stb

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

        for eachTMSID in dicPopularSearch.keys():
            args = {'TMS_ID': eachTMSID,
                    }
            sURL = sFullURL + '%(TMS_ID)s' % args
            oProgramDetail = Utils.GetHTTPResponse(sURL)
            sTitle = oProgramDetail['_source']['title']
            print sTitle


            #eachTMSID
            #dicPopularSearch[eachTMSID]
            #print eachTMSID
            #constructed_query = {"query":
            #     {"match": 
            #        {
            #            "tms_id": eachTMSID
            #        }
            #    }}
            #print constructed_query
            #result = tms.search(index='tms_movies_programs',doc_type='tms_movies_programs', body=constructed_query, size=10)
            #print "Result:", result

        #xSimple = "http://tms-catalog.dishanywhere.com:9200/tms_movies_programs/tms_movies_programs/_search"
        #oRes = Utils.GetHTTPResponse(xSimple)
        #print oRes

        #print "dicPopularSearch.keys()\n", dicPopularSearch.keys()
        #tms = elasticsearch.Elasticsearch(hosts = Constants.TMS_SEARCH_URL, connection_class = elasticsearch.ThriftConnection, timeout = 80)

#=============================================================================#
# End Of Class: stb
#=============================================================================#
