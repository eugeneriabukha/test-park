from KeywordDriver import Instruction
from Constants import Constants
from Encode import EncodeTitle
import stbt
import time

#=============================================================================#
# File: stb.py
#
#  Copyright (c) 2015, Vinoth Kumar Ravichandran, Prithvi Nath Manikonda
#  All rights reserved.
#
# Description: Classes and functions for set top box
#    These classes and functions are application dependent, performs activities based
#    on the user input from the instruction sheet
#
#    The keyword passed on from instruction sheet is analyzed and appropriate
#    class and its methods would be dynamically called based on instruction
#
#--
# Depends On:
#    KeywordDriver
#    Encode
#    Constants
#
#++
#=============================================================================#

# COMMON CONSTANTS
DEFAULT_SEARCH_CHAR = 'P'

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
    def __init__(self,oInstruction):
        self.instruction = oInstruction

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
# Class: Navigate
#
# Description: Functions for class Navigate
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
class Navigate:
    #=============================================================================#
    # Method: initialize()
    # Description: Initializes the service class with information required for running the test
    # Returns: NA
    # Usage Examples: STB.new(oInstruction)
    # where oInstruction should be of class Instruction
    #=============================================================================#
    def __init__(self,oInstruction):
        self.instruction = oInstruction

    #=============================================================================#
    # Method: Search
    # Description: 
    # Returns: NA
    # Usage Examples: 
    #=============================================================================#
    def Search(self):
        stbt.press('KEY_TV')
        stbt.press('KEY_MENU')
        stbt.press('KEY_DOWN')
        stbt.press('KEY_SELECT')

#=============================================================================#
# Class: Search
#
# Description: Functions for class Search
#    These functions and methods are platform dependent
#
#  Key:   () = No parameters,  (...) = parameters required
#
# Methods:
#   __init__(oInstruction)
#   EnterTitle()
#
# Pre-requisites:
# ++
#=============================================================================#
class Search:
    #=============================================================================#
    # Method: initialize()
    # Description: Initializes the service class with information required for running the test
    # Returns: NA
    # Usage Examples: STB.new(oInstruction)
    # where oInstruction should be of class Instruction
    #=============================================================================#
    def __init__(self,oInstruction):
        self.instruction = oInstruction

    #=============================================================================#
    # Method: 
    # Description: 
    # Returns: NA
    # Usage Examples: 
    #=============================================================================#
    def Title(self):
        # fetch data from the instruction
        oTestData = self.instruction.testdata_detailed
        sTitle = oTestData[Constants.SEARCH_COL_TITLE]
        bIncludeNetflix = oTestData[Constants.SEARCH_COL_INCLUDE_NETFLIX]
        print sTitle
        print bIncludeNetflix

        #sDirectInput = oTestData[Constants.DIRECT_INPUT]
        #lKeyStrokes = EncodeTitle(sDirectInput,DEFAULT_SEARCH_CHAR)
        #for keyStroke in lKeyStrokes:
        #    stbt.press(keyStroke)
            #time.sleep(0.05)

#=============================================================================#
# End Of Class: stb
#=============================================================================#