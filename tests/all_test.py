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

#def test_regression_sample1():
#	print "test_regression_sample1"
#
#def test_smoke_1():
#	print "test_smoke_1"
#
#def test_smoke_2():
#	print "test_smoke_2"
