from time import sleep
import stbt
import os

from scripts.Constants import *
from scripts.DataDriver import *
from scripts.CustomException import *
from scripts.KeywordDriver import *
from scripts.KeywordFactory import *

#=============================================================================#
# Method: test_smoke()
# Description: runs the list of smoke test cases provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_smoke():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_Smoke.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()

#=============================================================================#
# Method: test_z_03_mostPopular()
# Description: runs the list of keywords provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_z_03_mostPopular():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_TestCase03_MostPopular.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()

#=============================================================================#
# Method: test_z_05_09_singleCharacterSearch()
# Description: runs the list of keywords provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_z_05_09_singleCharacterSearch():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_TestCase05-09.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()

#=============================================================================#
# Method: test_z_10_HBO()
# Description: runs the list of keywords provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_z_10_HBO():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_TestCase10_HBO.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()

#=============================================================================#
# Method: test_z_11_13()
# Description: runs the list of keywords provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_z_11_13():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_TestCase11-13.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()

#=============================================================================#
# Method: test_z_14_Netflix()
# Description: runs the list of keywords provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_z_14_Netflix():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_TestCase14_Netflix.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()

#=============================================================================#
# Method: test_z_15_Sports()
# Description: runs the list of keywords provided in the instruction sheet
# Returns: NA
#=============================================================================#
def test_z_15_Sports():
    # Create an Object for DataDriver
    oDataDriver = DataDriver("Instructions_TestCase15_Sports.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()

