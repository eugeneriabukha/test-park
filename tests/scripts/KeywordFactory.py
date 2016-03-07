import importlib
from Constants import Constants
from CustomException import CustomException
#=============================================================================#
# File: KeywordFactory.py
#
#  Copyright (c) 2015, Vinoth Kumar Ravichandran, Joe DiMauro
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
#    Instruction Sheet (calls in the instruction sheet)
#    KeywordDriver
#    Constants
#
# Classes Added or Extended:
#    Constants (Constants.py)
#
#++
#=============================================================================#

#=============================================================================#
# Class: KeywordFactory
#=============================================================================#
#
# Description: Functions for KeywordFactory
#    These functions and methods are application and platform independent
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
#   Execute()
#
# Pre-requisites:
# ++
#=============================================================================#

class KeywordFactory:
  #=============================================================================#
  # Method: initialize()
  # Description: initializes the keywordfactory with one row of instruction
  # Returns: N/A
  # Usage Examples: oKeywordFactory = KeywordFactory(oInstruction)
  # where oInstruction should of type Instruction
  #=============================================================================#
  def __init__(self,oInstruction):
    # member variables
    self.instruction = oInstruction

  #=============================================================================#
  # Method: Execute()
  # Description: executes the specific instruction after analysis
  # Returns: N/A
  # Usage Examples: oKeywordFactory.Execute()
  #=============================================================================
  def Execute(self):
    # capturing the length of the keywords
    arKeyword = self.instruction.action.split(Constants.DELIMITER_STOP)
    oObject = ""
    iTotalCount = len(arKeyword)

    # currently only keywords of 2 levels are supported. analyzing the same
    if iTotalCount > 3:
        sTemp = "Keyword level cannot be greater than 3 <{%s}>" %(self.instruction.action)
        raise IndexError(sTemp)

    # Raises an error for unknown class or known class with unknown methods
    sModuleName = arKeyword[0]
    sClassName = arKeyword[1]
    sMethodName = arKeyword[2]
    oModule = __import__('scripts.'+ sClassName, fromlist=['*'])
    oClass = getattr(oModule,sClassName)
    oObject = oClass(self.instruction)
    getattr(oObject,sMethodName)()

#=============================================================================#
# End Of Class: KeywordFactory
#=============================================================================#
