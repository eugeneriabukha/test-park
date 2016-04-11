"""
.. module:: Common
   :platform: Unix, Windows
   :synopsis: module which holds common classes and functionality

.. moduleauthor:: Vinoth Kumar Ravichandran <vinoth.ravichandran@echostar.com>, Prithvi Manikonda <Prithvi.Manikonda@echostar.com>

"""
import urllib2
import json
import stbt
from Keywords import *
from collections import OrderedDict
import random
import string
import sys
from Logger import *

class cUtils:
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
        """
        global global_wait

        # press keystrokes for search
        for sKeyStroke in lListOfKeyStrokes:
            stbt.press(sKeyStroke)
            time.sleep(global_wait)
        time.sleep(Constants.LONG_WAIT)

    def SetHBOTitle(self,sHBOTitle):
        """
        This function saves the search HBO Title to be searched

        Args:
            sHBOTitle (string):  string containing the HBO search Title on screen
        """
        self.HBO_title = sHBOTitle

    def GetHBOTitle(self):
        """
        This function fetches the string saved as HBO searched Title

        Returns:
            (string):  string containing the HBO search Title
        """
        return self.HBO_title

    def SetSearchResults(self,oSearchResults):
        """
        This function saves the search results

        Args:
            oSearchResults (list):  list of dictionary with search results
        """
        self.search_results = oSearchResults

    def GetSearchResults(self):
        """
        This function fetches the values saved as search results

        Returns:
            (list):  list of dictionary with search results
        """
        return self.search_results

    def SetExpectedSearchResults(self,dicSearchResults):
        """
        This function saves the expected search results

        Args:
            oSearchResults (dict): dictionary with expected search results
        """
        self.expected_search_results = dicSearchResults

    def GetExpectedSearchResults(self):
        """
        This function fetches the values saved as expected search results

        Returns:
            (dict):  dictionary of expected search results
        """
        return self.expected_search_results

    def SetSelectedTitle(self, sTitle):
        """
        This function saves the selected title name

        Args:
            sTitle (str): name of the title selected
        """
        self.selected_title = sTitle

    def GetSelectedTitle(self):
        """
        This function fetches the values saved as selected title

        Returns:
            (dict):  dictionary of expected search results
        """
        return self.selected_title

    def GetHTTPResponse(self,sURL):
        """
        This function hits a URL and provides back the response to the calling script

        Args:
            sURL: URL to fetch response from

        Returns:
            (json):  http response of the provided URL

        Raises:
            Nothing
        """
        oResponse = urllib2.urlopen(sURL)
        oJSON = json.load(oResponse)
        return oJSON

    def GetTitleByType(self,oSearchResults,sInputType):
        """
        This function fetches the response title for the provided input type

        Args:
            oSearchResults (list):  list of dictionary with search results
            sInputType: Type to search for
        Returns:
            (list):  list of title(s) which matches provided type

        Raises:
            Nothing
        """
        return [title for title in oSearchResults if title["Type"] == sInputType]

    def GetTitleByTitle(self,oSearchResults,sInputTitle):
        """
        This function fetches the response title for the provided input type

        Args:
            oSearchResults (list):  list of dictionary with search results
            sInputType: Title to search for
        Returns:
            (list):  list of title(s) which matches provided type

        Raises:
            Nothing
        """
        return [title for title in oSearchResults if title["Title"] == sInputTitle]

    def GetTitleByID(self,oSearchResults,sInputID):
        """
        This function fetches the response title for the provided input type

        Args:
            oSearchResults (list):  list of dictionary with search results
            sInputID: ID to search for
        Returns:
            (list):  list of title(s) which matches provided type

        Raises:
            Nothing
        """
        return [sTitle for sTitle in oSearchResults if sTitle["ID"] == int(sInputID)]

    def CompareResults(self,dicExpectedSearchResults,lActualSearchResults):
        """
        This function compares the actual results with the expected results to find a one to one match

        Args:
            dicExpectedSearchResults (dictionary):  ordered dictionary with expected search results
            lActualSearchResults(list): list of dictionary with actual search results
        Returns:
            (boolean): based on comparison

        Raises:
            (boolean): based on comparison
        """
        # declaration of required variables for comparison
        lActualResultTitles =[]
        lExpectedResultTitles = dicExpectedSearchResults.keys()
        dicResults = {}
        listOfResults = []
        iCounter = 0

        # Fetching the titles on the screen into a list lActualResultTitles
        for eachSearchResult in lActualSearchResults:
            sTempTitle = str(self.GetTitleByID(lActualSearchResults,iCounter)[0]['Title'])
            lActualResultTitles.append(sTempTitle)
            iCounter = iCounter + 1

        bSuccess = True
        dictExpected = OrderedDict({})
        dictActual = OrderedDict({})
        for iCounter in range(0,10):
            dictExpected[lExpectedResultTitles[iCounter]] = ""
            dictActual[lActualResultTitles[iCounter]] = ""

        if dictExpected != dictActual:
            bSuccess = False

        # Printing comparison results
        Logger.note.info( "Comparison Results:")
        Logger.note.info( "Expected: %s" %dictExpected.keys())
        Logger.note.info( "Actual: %s"  %dictActual.keys())
        return bSuccess

    def FetchTextOfRegion(self, REGION, TESSERACT = None, FirstLineOnly = None):
        """
        this fetches the text on the specified region and provides back the details

        Args:
            REGION (dictionary):  a dictionary with x, y, height and width for finding a region
            TESSERACT(list): list of words to look for in the region
        Returns:
            (sTextFound): text found in the specified region

        Raises:
            Nothing
        """
        # fetch the region based on the region dictionary
        oRegion = self.FetchRegion(REGION)
        # based on provided input, fetch the text on the provided region
        if TESSERACT == None:
            sTextFound = stbt.ocr(region = oRegion)
        else:
            print TESSERACT
            sTextFound = stbt.ocr(region = oRegion, tesseract_user_words = TESSERACT)
        # trim the text captured before returning
        sTextFound = sTextFound.strip()
        # fetch the first line only when asked for
        if len(sTextFound)==0:
            Logger.note.error( "No text displayed on the screen.")
            return sTextFound
        if FirstLineOnly == True:
            sTextFound = sTextFound.splitlines()[0]
        return sTextFound

    def FetchRegion(self,REGION):
        """
        this fetches the specified region and returns the region

        Args:
            REGION (dictionary):  a dictionary with x, y, height and width for finding a region
            TESSERACT(list): list of words to look for in the region
        Returns:
            fetched region based on the provided parameters

        Raises:
            Nothing
        """
        # fetch the region based on the region dictionary
        oRegion = stbt.Region(x = REGION['x'], y = REGION['y'], width = REGION['width'], height = REGION['height'])
        return oRegion

    def MatchLogo(self,LOGO_LIST,REGION = None):
        """
        this fetches the specified region and tries to match if one of the provided logo is available from the provided list

        Args:
            REGION (dictionary):  a dictionary with x, y, height and width for finding a region
            LOGO_LIST(list): list of logo images which has to be tested
        Returns:
            fetches the provided region for which a logo is found

        Raises:
            Nothing
        """
        # if the region of the logo is provided, then region should be fetched
        if REGION != None:
            oRegion = self.FetchRegion(REGION)

        bFlag = False
        for sImage in LOGO_LIST:
            if REGION != None:
                oMatch = stbt.match(sImage,region = oRegion)
            else:
                oMatch = stbt.match(sImage)
            if oMatch.match == True:
                return oMatch.region

        if bFlag == False:
            #print "The expected logo was unavailable in the provided list of logos"
            return False   

    def GetRandomLetter(self):
        """
        this fetches the specified region and returns the region

        Returns:
            returns a upper case letter.

        """
        return random.choice(string.letters).upper()


# public instantition of the cUtils class to be used by other Classes
Utils = cUtils()

