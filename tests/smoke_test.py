from time import sleep
import stbt
import os

from scripts.Constants import *
from scripts.DataDriver import *
from scripts.CustomException import *
from scripts.KeywordDriver import *
from scripts.KeywordFactory import *

#=============================================================================#
# Method: test_keyworddriver()
# Description: runs the list of keywords provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_smoke():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_Smoke.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()
