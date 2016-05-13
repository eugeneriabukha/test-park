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
def test_keyworddriver():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_Smoke.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()

#=============================================================================#
# Method: test_run_demo()
# Description: runs the list of keywords provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_z_demo():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_Demo.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()

#=============================================================================#
# Method: test_()
# Description: runs the list of keywords provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_z_testing():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_Testing.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()
