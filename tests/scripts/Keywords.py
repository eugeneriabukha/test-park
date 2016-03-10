from KeywordDriver import Instruction
from Constants import Constants
import stbt
import time
import urllib2

#=============================================================================#
# File: Keywords.py
#
#  Copyright (c) 2015, Vinoth Kumar Ravichandran, Prithvi Nath Manikonda
#  All rights reserved.
#
# Description: Classes and functions for KeywordFactory
#    These classes and functions are application dependent, performs activities based
#    on the user input from the instruction sheet
#
#    The keyword passed on from instruction sheet is analyzed and appropriate
#    class and its methods would be dynamically called based on instruction
#
#--
# Depends On:
#    Instruction
#    KeywordDriver
#    Constants
#
# Classes Added or Extended:
#    Constants (Constants.py)
#    Instruction
#
#++
#=============================================================================#

#=============================================================================#
# Class: Service
#
# Description: Functions for class Service
#    These functions and methods are platform dependent
#
# Table of Contents
#
#  Please manually update this TOC with the alphabetically sorted names of the items in this module,
#  and continue to add new methods alphabetically into their proper location within the module.
#
#  Key:   () = No parameters,  (...) = parameters required
#
# Methods:
#   __init__(oInstruction)
#   TestCaseStart()
#   TestCaseEnd()
#   SampleDummyKeyword()
#   FailureKeyword()
#
# Pre-requisites:
# ++
#=============================================================================#
class Service:
    #=============================================================================#
    # Method: initialize()
    # Description: Initializes the service class with information required for running the test
    # Returns: NA
    # Usage Examples: Service.new(oInstruction)
    # where oInstruction should be of class Instruction
    #=============================================================================#
    def __init__(self,oInstruction):
        self.instruction = oInstruction

    #=============================================================================#
    # Method: TestCaseStart
    # Description: Intimates the start of a test case
    # Returns: NA
    # Usage Examples: Service.TestCaseStart
    #=============================================================================#
    def TestCaseStart(self):
        print "TestCase Start"
        oTestData = self.instruction.testdata_detailed
        sDirectInput = oTestData[Constants.DIRECT_INPUT]
        print "Direct Input Data: %s" %(sDirectInput)

    #=============================================================================#
    # Method: TestCaseEnd
    # Description: Intimates the end of a test case
    # Returns: NA
    # Usage Examples: Service.TestCaseEnd
    #=============================================================================#
    def TestCaseEnd(self):
        print "TestCase End"

    #=============================================================================#
    # Method: SampleDummyKeyword
    # Description: Sample dummy Keyword
    # Returns: NA
    # Usage Examples: Service.SampleDummyKeyword
    #=============================================================================#
    def SampleDummyKeyword(self):
        print "Sample Dummy Keyword"

    #=============================================================================#
    # Method: FailureKeyword
    # Description: a sample failure keyword
    # Returns: NA
    # Usage Examples: Service.FailureKeyword
    #=============================================================================#
    def FailureKeyword(self):
        print "FailureKeyword"
        self.instruction.actualresult = "UnExpectedResult"

#=============================================================================#
# End Of Class: Service
#=============================================================================#

#=============================================================================#
# Class: AccessData
#
# Description: Functions for class DataAccess
#    These functions and methods are platform dependent
#
#  Key:   () = No parameters,  (...) = parameters required
#
# Methods:
#   __init__(oInstruction)
#   FetchData()
#
# Pre-requisites:
# ++
#=============================================================================#
class AccessData:
    #=============================================================================#
    # Method: initialize()
    # Description: Initializes the service class with information required for running the test
    # Returns: NA
    # Usage Examples: Service.new(oInstruction)
    # where oInstruction should be of class Instruction
    #=============================================================================#
    def __init__(self,oInstruction):
        self.instruction = oInstruction

    #=============================================================================#
    # Method: FetchData
    # Description: Launches specific browser
    # Returns: NA
    # Usage Examples: Service.LaunchBrowser
    #=============================================================================#
    def FetchData(self):
        #fetches the URL to launch
        oTestData = self.instruction.testdata_detailed
        for dValue in oTestData.values():
            sUserName = dValue["UserName"]
            sPassword = dValue["Password"]
            print "Provided data: %s | %s" %(sUserName,sPassword)

        # Updates success on successful launch of browser
        self.instruction.actualresult = self.instruction.expectedresult

    #=============================================================================#
    # Method: GoToInternet
    # Description: Fetch details from internet
    # Returns: NA
    # Usage Examples: 
    #=============================================================================#
    def GoToInternet(self):
        response = urllib2.urlopen('http://www.google.com/')
        html = response.read()
        print html

#=============================================================================#
# End Of Class: AccessData
#=============================================================================#

#=============================================================================#
# Class: Common
#
# Description: Functions for class Common
#    These functions and methods are platform dependent
#
#  Key:   () = No parameters,  (...) = parameters required
#
# Methods:
#   __init__(oInstruction)
#   ()
#
# Pre-requisites:
# ++
#=============================================================================#
class Common:
    #=============================================================================#
    # Method: initialize()
    # Description: Initializes the service class with information required for running the test
    # Returns: NA
    # Usage Examples: STB.new(oInstruction)
    # where oInstruction should be of class Instruction
    #=============================================================================#
    def __init__(self, oInstruction):
        self.instruction = oInstruction
        self.global_wait = Constants.NO_WAIT

    #=============================================================================#
    # Method: set_global_wait()
    # Description: sets the global wait
    # Returns: NA
    # Usage Examples: 
    # where 
    #=============================================================================#
    def SetGlobalWait(self):
        # fetch value for the global wait
        oTestData = self.instruction.testdata_detailed
        sWait = oTestData[Constants.DIRECT_INPUT]

        # find the input type and set the global wait based on the provided value
        if sWait == "NO_WAIT":
            self.global_wait = Constants.NO_WAIT
        elif sWait == "SHORT_WAIT":
            self.global_wait = Constants.SHORT_WAIT
        elif sWait == "MEDIUM_WAIT":
            self.global_wait = Constants.MEDIUM_WAIT
        elif sWait == "LONG_WAIT":
            self.global_wait = Constants.LONG_WAIT
        else:
            try:
                self.global_wait = int(sWait)
            except ValueError:
                self.global_wait = Constants.SHORT_WAIT
                print "Kindly check the value used for setting global wait. Defaulting to SHORT_WAIT"

    #=============================================================================#
    # Method: PressViewTV
    # Description: 
    # Returns: NA
    # Usage Examples: 
    #=============================================================================#
    def PressViewTV(self):
        stbt.press('KEY_TV') # Switches to live tv
        assert stbt.wait_for_motion()
        self.instruction.actualresult = self.instruction.expectedresult

    #=============================================================================#
    # Method: 
    # Description: 
    # Returns: NA
    # Usage Examples: 
    #=============================================================================#
    def PressMenu(self):
        stbt.press('KEY_MENU')  # Close any open menus
        assert stbt.wait_for_motion()
        self.instruction.actualresult = self.instruction.expectedresult

    #=============================================================================#
    # Method: 
    # Description: 
    # Returns: NA
    # Usage Examples: 
    #=============================================================================#
    def PressKey(self,sKey):
        stbt.press(sKey)

#=============================================================================#
# End Of Class: Common
#=============================================================================#