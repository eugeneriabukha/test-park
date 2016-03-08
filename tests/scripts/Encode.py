#=============================================================================#
# File: Encode.py
#
#  Copyright (c) 2016, Prithvi Nath Manikonda, Vinoth Kumar Ravichandran
#  All rights reserved.
#
# Description: Functions and methods for Encode functionality
#    These functions and methods are application and platform independent, and
#    are NOT specific to Web based applications.
#
# Modules:
#
# Classes Added or Extended:
#    Constants
#
#=============================================================================#

#=============================================================================#
# Require and Include section
# Entries for additional files or methods needed by these methods
#=============================================================================#
from Constants import Constants as C

#=============================================================================#
# Class: EncodeWord
#=============================================================================#

class EncodeWord(list):
    #=============================================================================#
    # Method: __init__(self, sWord, InitialCharacter)
    # Description:
    # Variables:    sWord: 
    #               InitialCharacter: 
    #=============================================================================#
    def __init__(self, sWord, sInitialCharacter):
        self.charmap = C.CHARACTER_MAP
        self.word = sWord
        self.ListofTuples = []
        self.DiffTuple = []
        self.ListofInst = []
        self.InitialCharacter = sInitialCharacter
        self.InitialCharacterTuple = self.getCoordinates(self.InitialCharacter)
        self.StringArray = self.returnStringArray(self.word)

        for iCounter in self.StringArray:
            self.ListofTuples.append(self.getCoordinates(iCounter))

        self.getDiff(self.ListofTuples)
        self.getKeyStrokes(self.DiffTuple)
        self.InitialCharacterTuple = self.getCoordinates(iCounter)

        for Inst in self.ListofInst:
            self.append(Inst)

    #=============================================================================#
    # Method: returnStringArray(self, sWord)
    # Description : 
    # Variables :    sWord: 
    #=============================================================================#
    def returnStringArray(self, sWord):
        self.word = sWord.upper()
        return list(self.word)

    #=============================================================================#
    # Method: getCoordinates(self, sCharacter)
    # Description : 
    # Variables :    sCharacter: 
    #=============================================================================#
    def getCoordinates(self, sCharacter):
        return self.charmap[sCharacter]

    #=============================================================================#
    # Method: getDiff(self, ListofTuples)
    # Description : 
    # Variables :    sCharacter: 
    #=============================================================================#
    def getDiff(self, ListofTuples):
        iCounter = 0
        for tuple in ListofTuples:
            if iCounter == 0:
                diff = (ListofTuples[0][0]-self.InitialCharacterTuple[0],ListofTuples[0][1]-self.InitialCharacterTuple[1])
                self.DiffTuple.append(diff)
            else:
                diff = (ListofTuples[iCounter][0]-ListofTuples[iCounter-1][0],ListofTuples[iCounter][1]-ListofTuples[iCounter-1][1])
                self.DiffTuple.append(diff)
            iCounter = iCounter + 1

    #=============================================================================#
    # Method: getKeyStrokes(self,DiffTuple)
    # Description : 
    # Variables :    DiffTuple: 
    #=============================================================================#
    def getKeyStrokes(self, DiffTuple):
        for diff in DiffTuple:
            if diff[0] > 0:
                for iCounter in range(0,abs(diff[0])):
                    self.ListofInst.append("KEY_DOWN")
            if diff[0] <= 0:
                for iCounter in range(0,abs(diff[0])):
                    self.ListofInst.append("KEY_UP")
            if diff[1] > 0:
                for iCounter in range(0,abs(diff[1])):
                    self.ListofInst.append("KEY_RIGHT")
            if diff[1] <= 0:
                for iCounter in range(0,abs(diff[1])):
                    self.ListofInst.append("KEY_LEFT")
            self.ListofInst.append("KEY_SELECT")

#=============================================================================#
# Class: EncodeTitle
#=============================================================================#
class EncodeTitle(list):
    #=============================================================================#
    # Method: __init__(self, sWord, InitialCharacter)
    # Description:
    # Variables:    sProgramName: 
    #               InitialCharacter: 
    #=============================================================================#
    def __init__(self, sProgramName,sInitialCharacter):
        sProgramName = sProgramName.uppercase
        self.ProgramName = sProgramName
        self.InitialCharacter = sInitialCharacter
        self.ListofWord = self.ProgramName.split()
        self.InitialCharacter = sInitialCharacter
        InteratorWords = 0
        self.InstructionSet = []
        for Word in self.ListofWord:
            if InteratorWords == 0:
                for Inst in EncodeWord(Word,self.InitialCharacter):
                    self.InstructionSet.append(Inst)
            else:
                for Inst in EncodeWord(Word,self.ListofWord[InteratorWords-1][-1]):
                    self.InstructionSet.append(Inst)
            InteratorWords = InteratorWords+1
            if InteratorWords < len(self.ListofWord):
                self.InstructionSet.append('KEY_PAUSE')
        for Inst in self.InstructionSet:
            self.append(Inst)

