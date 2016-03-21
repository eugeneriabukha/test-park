"""
.. module:: Common
   :platform: Unix, Windows
   :synopsis: module which holds common classes and functionality

.. moduleauthor:: Vinoth Kumar Ravichandran <vinoth.ravichandran@echostar.com>, Prithvi Manikonda <Prithvi.Manikonda@echostar.com>

"""
import urllib2
import json
from Keywords import *

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
        print oJSON
        return oJSON

'''
Helpful in future
list1=[{'id':1,'name':'hello','type':'TV'},{'id':2,'name':'hel','type':'TV'}]
#print list1
print [item for item in list1 if item["type"] == 'TV']'''

# public instantition of the cUtils class to be used by other Classes
Utils = cUtils()

