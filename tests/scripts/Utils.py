"""
.. module:: Common
   :platform: Unix, Windows
   :synopsis: module which holds common classes and functionality

.. moduleauthor:: Vinoth Kumar Ravichandran <vinoth.ravichandran@echostar.com>, Prithvi Manikonda <Prithvi.Manikonda@echostar.com>

"""
import urllib2
import json
from Keywords import *
from collections import OrderedDict

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

    def SetSearchResults(self,oSearchResults):
        """
        This function saves the search results

        Args:
            oSearchResults (list):  list of dictionary with search results

        Returns:
            Nothing

        Raises:
            Nothing
        """
        self.search_results = oSearchResults

    def GetSearchResults(self):
        """
        This function fetches the values saved as search results

        Args:
            Nothing

        Returns:
            (list):  list of dictionary with search results

        Raises:
            Nothing
        """
        return self.search_results

    def SetExpectedSearchResults(self,dicSearchResults):
        """
        This function saves the expected search results

        Args:
            oSearchResults (dict): dictionary with expected search results

        Returns:
            Nothing

        Raises:
            Nothing
        """
        self.expected_search_results = dicSearchResults

    def GetExpectedSearchResults(self):
        """
        This function fetches the values saved as expected search results

        Args:
            Nothing

        Returns:
            (dict):  dictionary of expected search results

        Raises:
            Nothing
        """
        return self.expected_search_results

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

    def CompareResults(self,oExpectedSearchResults,oActualSearchResults):
        """
        This function compares the actual results with the expected results

        Args:
            oExpectedSearchResults (list):  list of ordered dictionary with expected search results
            oActualSearchResults(list): list of dictionary with actual search results
        Returns:
            (list):  list of title(s) which matches provided type

        Raises:
            Nothing
        """
        iCounter = 0
        oActualResultTitles =[]
        oExpectedResultTitles=oExpectedSearchResults.keys()
        ResultDict = {}
        ListofDict=[]
        for eachSearchResult in oActualSearchResults:
            oActualResultTitles.append(self.GetTitleByID(oActualSearchResults,iCounter)[0]['Title'])
            iCounter = iCounter + 1
        iCounter = 0
        for iCounter in range(0,10):
            ResultsDict["Expected"] = ExpectedResultTitles[i]
            ResultsDict["Actual"] = oActualResultTitles[i]
            if oActualResultTitles[i]==oExpectedResultTitles[i]:
                ResultsDict["Result"] = 'Sucess'
            else:
                ResultsDict["Result"] = 'Failure'
            # Appending the results dict into the list
            ListofDict.append(ResultsDict.copy())
        print ListofDict



# public instantition of the cUtils class to be used by other Classes
Utils = cUtils()

