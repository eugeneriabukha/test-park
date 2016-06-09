from Constants import Constants
from DataDriver import DataDriver
from KeywordFactory import KeywordFactory
from CustomException import CustomException
from Logger import *
import collections
import time
import datetime
import os
import re
import cv2
import stbt
import re
#=============================================================================#
# File: KeywordDriver.py
#
#  Copyright (c) 2015, Vinoth Kumar Ravichandran, Prithvi Nath Manikonda
#  All rights reserved.
#
# Description: Functions and methods for Keyword Driver Scripts
#    These functions and methods are application and platform independent, and
#    are NOT specific to Web based applications.
#
#
#    Some of these methods and functions have been collected from, or based upon
#    Open Source versions found on various sites in the Internet, and are noted.
#
# Modules:
#
# Classes Added or Extended:
# KeywordDriver
# InstructionList
# Instruction
# Options
# Execution
# CustomException
#
#=============================================================================#

#=============================================================================#
# Require and Include section
# Entries for additional files or methods needed by these methods
#=============================================================================#
#    Constants
#    DataDriver
#    KeywordFactory
#=============================================================================#

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]
#=============================================================================#
# Class: KeywordDriver
#=============================================================================#
class KeywordDriver(dict):
    #=============================================================================#
    # Method: __init__(self, oDataDriver)
    # Description: initialize is the first function that would be call when the class is
    # instantiated
    # Returns: NA
    # Usage Examples: NA
    #=============================================================================#
    def __init__(self, oDataDriver):
        # initialize the parameters before use
        iCounter = 1
        iTCCounter = 1
        sLabel = ""
        sAction = ""
        sTestData = ""
        sOptions = ""
        sExpectedResult = ""
        sActualResult = ""
        #sExpectedMessage = ""
        sComments = ""
        dirLables={}
        #Logger.note.debug('Analyzing the data to create an instruction object')
        # Analyze the data to create an instruction object
        for sDDKey, oDDValue in oDataDriver.iteritems():
            for oInstructionName, oInstructionValue in oDDValue.iteritems():
                # Create a label if the provided label is empty
                if(oInstructionName == Constants.LABEL):
                    sLabel = str(iCounter) + Constants.DELIMITER_HIFEN + Constants.INSTRUCTION + Constants.DELIMITER_HIFEN + oInstructionValue
                    sInstructionName = str(iCounter) + Constants.DELIMITER_HIFEN + Constants.INSTRUCTION
                    if oInstructionValue=="":
                        sLabel = str(iCounter) + Constants.DELIMITER_HIFEN + Constants.INSTRUCTION            
                # segregate action of the provided instruction
                elif(oInstructionName == Constants.ACTION):
                    sAction = oInstructionValue
                # segregate test data of the provided instruction
                elif(oInstructionName == Constants.TESTDATA):
                    sTestData = oInstructionValue
                # segregate options of the provided instruction
                elif(oInstructionName == Constants.OPTIONS):
                    sOptions = oInstructionValue
                # segregate expected result of the provided instruction
                elif(oInstructionName == Constants.EXPECTED_RESULT):
                    sExpectedResult = oInstructionValue
                # segregate actual result of the provided instruction
                elif(oInstructionName == Constants.ACTUAL_RESULT):
                    pass
                # segregate expected message of the provided instruction
                #elif(oInstructionName == Constants.EXPECTED_MESSAGE):
                    #sExpectedMessage = oInstructionValue
                # segregate comments of the provided instruction
                elif(oInstructionName == Constants.COMMENTS):
                    sComments = oInstructionValue
                else:
                    Logger.note.info('"Unrecognized column name in Instruction Sheet <%s>" % (oInstructionName)')
                    sTemp = "Unrecognized column name in Instruction Sheet <%s>" % (oInstructionName)
                    raise Exception(sTemp)

            # Create a dynamic test case name if it does not exist
            sTCName = Constants.TESTCASE + Constants.DELIMITER_UNDERSCORE + str(iTCCounter)
            sTCStart = Constants.SERVICE + Constants.DELIMITER_STOP + Constants.TESTCASE_START

            # if action is start of the test case, count the test case
            bMatch = re.search(sTCStart, sAction)
            if(bMatch == True):
                sLabel = sTCName
                iTCCounter = iTCCounter + 1

            # Create an instruction object before passing
            #oInstruction = Instruction(sLabel,sComments,sAction,sTestData,sOptions,sExpectedResult,sExpectedMessage)
            oInstruction = Instruction(sLabel,sComments,sAction,sTestData,sOptions,sExpectedResult)
            if dirLables.has_key(''.join(sLabel.split(Constants.DELIMITER_HIFEN)[1:])):
                sTemp = "Label cannot be duplicated <%s>. Please check row <%s> in instruction sheet" %(sLabel,iCounter)
                raise Exception(sTemp)
            else:
                if ''.join(sLabel.split(Constants.DELIMITER_HIFEN)[1:]) != Constants.INSTRUCTION:
                    dirLables[''.join(sLabel.split(Constants.DELIMITER_HIFEN)[1:])] = 1
            # add the created instruction in keyword driver
            self[sLabel] = oInstruction
            iCounter = iCounter + 1

        # perform analysis of the created list of instructions
        self.Analyze()

    #=============================================================================#
    # Method: Analyze()
    # Description: Analyzes the provided set of instructions
    # Returns: boolean
    #=============================================================================#
    def Analyze(self):
        # initialize before analysis
        dTemp = self
        iCountTCStart = 0
        iCountTCEnd = 0

        # check if total number of test case start has its end
        sTCStart = Constants.SERVICE + Constants.DELIMITER_STOP + Constants.TESTCASE_START
        sTCEnd = Constants.SERVICE + Constants.DELIMITER_STOP + Constants.TESTCASE_END
        for instructionRow in dTemp.values():
            # fetch action for collecting counters
            sAction = instructionRow.action
            bMatchTCStart = re.search(sTCStart,sAction)
            bMatchTCEnd = re.search(sTCEnd,sAction)
            # increase counters based on test case start and end
            if bMatchTCStart == True:
                iCountTCStart = iCountTCStart + 1
            if bMatchTCEnd == True:
                iCountTCEnd = iCountTCEnd + 1

        # raise an exception if number of start do not have its end
        if iCountTCStart != iCountTCEnd:
            #Logger.note.info('Every test case start do NOT have an end or vice versa. Kindly check instructions sheet')
            raise Exception("Every test case start do NOT have an end or vice versa. Kindly check instructions sheet")

        return True

    #=============================================================================#
    # Method: PrettyPrint()
    # Description: pretty print the keyword driver
    # Returns: NA
    #=============================================================================#
    def PrettyPrint(self):
        dTemp = self
        # Print each instruction added to keyword driver
        for oInstructionRow in sorted(dTemp.values()):
             Logger.note.info( oInstructionRow.PrettyPrint() )

    #=============================================================================#
    # Method: Execute()
    # Description: executes the provided list of keywords
    # Returns: N/A
    # Usage Examples:
    #=============================================================================#
    def Execute(self):
        Execution(self)

#=============================================================================#
# Class: InstructionList
#=============================================================================#
class InstructionList(dict):
    #=============================================================================#
    # Method: add(self,name, instruction)
    # Description: first function to be called when the class is instantiated
    # Returns:
    # Usage Examples:
    #=============================================================================#
    def add(self,sInstructionName, oInstruction):
      if isinstance(oInstruction,Instruction):
            self[sInstructionName] = oInstruction

#=============================================================================#
# Class: Instruction
#=============================================================================#
#
class Instruction:
    #=============================================================================#
    # Method: __init__
    # Description: first function to be called when the class is instantiated
    # Returns:
    # Usage Examples:
    #=============================================================================#
    #def __init__(self,sLabel,sComments,sAction,sTestData,sOptions,sExpectedResult,sExpectedMessage):
    def __init__(self,sLabel,sComments,sAction,sTestData,sOptions,sExpectedResult):
        self.label = sLabel
        self.comments = sComments
        self.action = sAction
        self.testdata = sTestData
        self.testdata_detailed = dict()
        self.options_detailed = Options(sOptions)
        self.expectedresult = sExpectedResult
        self.actualresult = ""
        self.elapsed_time = ""
        self.start_time = ""
        #self.expectedmessage = sExpectedMessage
        self.status = Constants.STATUS_NOT_EXECUTED
        self.execute = True

    #=============================================================================#
    # Method: get_options_detailed
    # Description: getter for options_detailed
    #=============================================================================#
    def get_options_detailed(self):
        return self.options_detailed

    #=============================================================================#
    # Method: set_testdata_detailed(self,testdata_detailed)
    # Description: setter for testdata_detailed
    #=============================================================================#
    def set_testdata_detailed(self,testdata_detailed):
        self.testdata_detailed = testdata_detailed

    #=============================================================================#
    # Method: get_variables(self)
    # Description: pretty prints the list of available variables
    #=============================================================================#
    def PrettyPrint(self):
        return "Label: %s| Action: %s | TestData: %s | TestData_Detailed: %s | Options: %s | ExpectedResult: %s | ActualResult: %s  | Status: %s | Comments: %s" \
        %(self.label, self.action, self.testdata, self.testdata_detailed, self.options_detailed, self.expectedresult, self.actualresult, self.status, self.comments)

#=============================================================================#
# Class: Options
#=============================================================================#
#
class Options(dict):
    #=============================================================================#
    # Method: __init__
    # Description: first function to be called when the class is instantiated
    #=============================================================================#
    def __init__(self,sOptions):
        # when an empty string is returned to analyze, return without analysis
        if (sOptions == ""):
            return

        # segregate the list of options separated by semi colon
        arOptions = sOptions.split(Constants.DELIMITER_SEMICOLON)
        hReturn = collections.OrderedDict()
        # analyze the provided list of options one by one
        for sOption in arOptions:
            arOptionDetail = sOption.split(Constants.DELIMITER_EQUAL)
            sOrder = ""
            sTempOption = str(arOptionDetail[0]).strip()
            # order the list of provided options
            if Constants.OPTIONS_ORDER.has_key(sTempOption):
                sOrder = Constants.OPTIONS_ORDER[sTempOption]
            elif(sTempOption == ""):
                pass
            else:
                # raise exception for Unrecognized options
                sTemp = "Every option used should be defined. Please register the following option <%s>" % (sTempOption)
                Logger.note.info('"Every option used should be defined. Please register the following option <%s>" % (sTempOption)')
                raise Exception(sTemp)

            hReturn[str(sOption)]=(sOrder)
        self.update(hReturn)

#=============================================================================#
# Class: Execution
#=============================================================================#
#
class Execution:
    #=============================================================================#
    # Method: __init__
    # Description: first function to be called when the class is instantiated
    #=============================================================================#
    def __init__(self,dicInstructions):
        """
        Initializes the execution class with information required for running the test

        Args:
            dicInstructions: dictionary of instructions to execute

        Returns:
            Nothing

        Raises:
            Nothing
        """
        self.instructionsDict = dicInstructions
        self.previousLabel = ""

        #self.CurrentTestCase = ""
        # Set expected messages
        #oExpectedMM = MessageManager(Constants.EXPECTED_RESULT)
        #self.ExpectedMessages = oExpectedMM

        # collect actual messages
        #oActualMM = MessageManager(Constants.ACTUAL_RESULT)
        #self.ActualMessages = oActualMM

        self.PerformExecution()
        self.FetchResults()

    def PerformExecution(self):
        """
        Functions required for performing Navigation

        Args:
            NA

        """
        sPrevInstructionName = ""
        sInstructionName = ""
        bRun = True
        tStartTime = ""
        sCurrentTestCase = ""

        # check if its start of a test case and perform actions accordingly
        sTCStart = Constants.SERVICE + Constants.DELIMITER_STOP + Constants.TESTCASE_START
        sTCEnd = Constants.SERVICE + Constants.DELIMITER_STOP + Constants.TESTCASE_END
        aList = sorted(self.instructionsDict.keys(),key=natural_keys)
        # run each instruction one by one
        for sPresentInstructionName in (aList):
            sPrevInstructionName = sInstructionName
            oInstruction = self.instructionsDict[sPresentInstructionName]

            # update current test case name if found
            if bool(re.search(sTCStart, oInstruction.action)) == True:
                tStartTime = time.time()
                tFormatStartTime = time.ctime(int(tStartTime))
                sCurrentTestCase = sPresentInstructionName
                Logger.note.debug("Start Time: %s" % tFormatStartTime)
            elif bool(re.search(sTCEnd, oInstruction.action)) == True:
                tDeltaSeconds = (time.time() - tStartTime)
                tTrimDownDeltaSeconds = "%.2f" % tDeltaSeconds
                Logger.note.debug("Elapsed Time: %.2f seconds" % tDeltaSeconds)
                oTCInstruction = self.instructionsDict[sCurrentTestCase]
                oTCInstruction.start_time = tFormatStartTime
                oTCInstruction.elapsed_time = tTrimDownDeltaSeconds
                #self.CurrentTestCase = sPresentInstructionName
                #self.ExpectedMessages.Add(sPresentInstructionName,oInstruction.expectedmessage)

            # fetch the instruction name for the provided item
            sInstructionName = [sKey for sKey, sValue in self.instructionsDict.items() if sValue == oInstruction][0]
            try:
                # if its start of the test case, run the test case
                if bRun == False:
                    bRun = re.search(sTCStart, oInstruction.action)
                    bRun = bool(bRun)
                    if bRun == False:
                        continue

                self.Execute(sPrevInstructionName,oInstruction)
            except CustomException as oException:
                if oException.name == Constants.EXIT_TC_ON_ERROR:
                    Logger.note.debug("Exiting test case because of an error in the current test step")
                    bRun = False
                else:
                    raise Exception(Constants.EXIT_ON_ERROR)

    def FetchResults(self):
        """
        Fetch results from the keyword driver and set it into an excel sheet

        Args:
            NA

        """
        sTCStart = Constants.SERVICE + Constants.DELIMITER_STOP + Constants.TESTCASE_START
        sTCEnd = Constants.SERVICE + Constants.DELIMITER_STOP + Constants.TESTCASE_END
        aList = sorted(self.instructionsDict.keys(),key=natural_keys)
        iTCCounter = 0
        bTCFlag = False
        lStatus = []
        dicTCStatus = collections.OrderedDict()
        dicTCElapsedTime = collections.OrderedDict()
        dicTCCreatedTime = collections.OrderedDict()
        sTestCaseName = ""
        iTotalElapsed = 0

        # fetching result after execution
        for sPresentInstructionName in (aList):
            oInstruction = self.instructionsDict[sPresentInstructionName]
            sInstructionName = [sKey for sKey, sValue in self.instructionsDict.items() if sValue == oInstruction][0]
            #Logger.note.debug(oInstruction.PrettyPrint())

            if re.search(sTCStart, oInstruction.action):
                iTCCounter = iTCCounter + 1
                bTCFlag = True
                sTestCaseName = oInstruction.testdata
                dicTCStatus[sTestCaseName] = ""
                Logger.note.debug("TestCase Start: %s" %sTestCaseName)
                sElapsedTime = oInstruction.elapsed_time
                iTotalElapsed = iTotalElapsed + float(sElapsedTime)
                Logger.note.debug("Elapsed time: %s" % sElapsedTime)
                sStartTime = oInstruction.start_time
                Logger.note.debug("Start time: %s" % sStartTime)
                dicTCElapsedTime[sTestCaseName] = sElapsedTime
                dicTCCreatedTime[sTestCaseName] = sStartTime

            elif re.search(sTCEnd, oInstruction.action):
                bTCFlag = False
                if Constants.STATUS_FAILURE in lStatus:
                    dicTCStatus[sTestCaseName] = Constants.STATUS_FAILURE
                elif Constants.STATUS_SKIPPED in lStatus:
                    dicTCStatus[sTestCaseName] = Constants.STATUS_SKIPPED
                else:
                    dicTCStatus[sTestCaseName] = Constants.STATUS_SUCCESS

                del lStatus[:]

                Logger.note.debug("TestCase End: %s" %sTestCaseName)
            else:
                if bTCFlag == True:
                    lStatus.append(oInstruction.status)
            
        Logger.note.debug("Test Case Dictionary: %s" % dicTCStatus)
        Logger.note.debug("Test Case Dictionary: %s" % dicTCElapsedTime)
        Logger.note.debug("Test Case Dictionary: %s" % dicTCCreatedTime)

        Logger.note.debug("Total Elapsed Time: %s" % iTotalElapsed)

        listOfTestCases = dicTCStatus.keys()
        Logger.note.info("|Test Case Name|Execution Status|Executed Time|Elapsed Time(seconds)")
        for eachTestCase in listOfTestCases:
            Logger.note.info("|%s|%s|%s|%s" %(eachTestCase,dicTCStatus[eachTestCase],dicTCCreatedTime[eachTestCase],dicTCElapsedTime[eachTestCase]))


        import logging

        LOG_FILENAME = 'logging_example.out'
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.DEBUG,
                            )

        logging.debug('This message should go to the log file')

        f = open(LOG_FILENAME, 'w')
        try:
            body = f.read()
        finally:
            f.close()

        print 'FILE:'
        print body

        #Logger.note.debug(self.ExpectedMessages.Message())
        #Logger.note.debug(self.ActualMessages.Message())

    #=============================================================================#
    # Method: get_previousLabel
    # Description: getter for previousLabel
    #=============================================================================#
    def get_previousLabel(self):
        return self.previousLabel

    #=============================================================================#
    # Method: set_previousLabel(self,previousLabel)
    # Description: setter for previousLabel
    #=============================================================================#
    def set_previousLabel(self,previousLabel):
        self.previousLabel = previousLabel

    #=============================================================================#
    # Method: PrettyPrint(self)
    # Description: PrettyPrints all the variables in the class
    #=============================================================================#
    def PrettyPrint(self):
        return "%s | %s | %s " %(self.instructionName,self.instruction,self.previousLabel)

    #=============================================================================#
    # Method: Execute(self,sPrevInstructionName)
    # Description: Executes the provided instruction
    #=============================================================================#
    def Execute(self,sPrevInstructionName,oExecutedInstruction):
        # perform pre-evaluation before running an instruction
        self.previousLabel = sPrevInstructionName
        bTakeScreenshot = True

        # performing pre dependency check
        try:
            self.EvaluatePreDependency(oExecutedInstruction)
        except CustomException as oException:
            bTakeScreenshot = False

        # instantiate a specific instruction and perform the execution
        if oExecutedInstruction.execute == True:
            oKeywordFactory = KeywordFactory(oExecutedInstruction)
            sReturnValue = oKeywordFactory.Execute()
            #self.ActualMessages.Add(self.CurrentTestCase,sReturnValue)
        else:
            Logger.note.debug("Skipping execution of the instruction")
            bTakeScreenshot = False

        # perform post dependency evaluation
        try:
            self.EvaluatePostDependency(oExecutedInstruction,bTakeScreenshot)
        except CustomException as oException:
            raise CustomException(oException.name)

        # Update the changes to instruction
        sInstructionName = [sKey for sKey, sValue in self.instructionsDict.items() if sValue == oExecutedInstruction][0]
        self.instructionsDict[sInstructionName] = oExecutedInstruction

    #=============================================================================#
    # Method: EvaluatePreDependency(self)
    # Description: Evaluates the dependecies of the provided instruction
    #=============================================================================#
    def EvaluatePreDependency(self,oExecutedInstruction):
        # fetch instruction name
        # pre-dependency before running an instruction
        Logger.note.debug("Evaluting pre dependency")

        sInstructionName = [sKey for sKey, sValue in self.instructionsDict.items() if sValue == oExecutedInstruction][0]
        arTemp = oExecutedInstruction.get_options_detailed()
        arSorted = sorted(arTemp,key=arTemp.get)

        Logger.note.debug("Instruction Name: %s" %sInstructionName)
        Logger.note.debug("Executed Instruction: %s" %oExecutedInstruction.PrettyPrint())

        # Fetch each option and execute based on provided options for the specific keyword
        for sOptionsKey in arSorted:
            arOptionDetail = sOptionsKey.split(Constants.DELIMITER_EQUAL)
            sTempLabel = ""
            # do not execute if the provided instruction is a comment
            if arOptionDetail[0] == Constants.COMMENT:
                oExecutedInstruction.execute = False
                self.instructionsDict[sInstructionName] = oExecutedInstruction
                return
            # evaluate dependency for presence of option DependsOn
            elif arOptionDetail[0] == Constants.DEPENDS_ON:
                # fetch previous label if DependsOn=Above
                if arOptionDetail[1] == Constants.ABOVE:
                    sTempLabel = self.previousLabel
                else:
                    sTempLabel = [sKey for sKey, sValue in self.instructionsDict.iteritems() if arOptionDetail[1] in sKey][0]

                # fetch status of dependent keyword
                try:
                    sDependencyStatus = self.instructionsDict[sTempLabel].status
                except KeyError:
                    sTemp = "The provided label do not exist <%s>" %(sTempLabel)
                    Logger.note.info(sTemp)

                    self.instructionsDict[sInstructionName] = oExecutedInstruction
                    raise Exception(sTemp)

                # execute the current only if the dependent keyword was a success
                if sDependencyStatus != Constants.STATUS_SUCCESS:
                    sTemp = "Dependency Failure : Dependent step failed for Instruction <"+ (sInstructionName)+">"
                    Logger.note.info(sTemp)
                    oExecutedInstruction.status = Constants.STATUS_SKIPPED
                    oExecutedInstruction.execute = False
                    self.instructionsDict[sInstructionName] = oExecutedInstruction
                    raise CustomException(Constants.DEPENDENCY_FAILURE)

            # directly pass the input for option: DirectInput
            elif arOptionDetail[0] == Constants.DIRECT_INPUT:
                hTemp = { Constants.DIRECT_INPUT : oExecutedInstruction.testdata }
                Logger.note.debug("Direct Input: %s" % hTemp)
                oExecutedInstruction.set_testdata_detailed(hTemp)

        # Fetch the data if directinput option is provided
        if ((oExecutedInstruction.options_detailed.has_key(Constants.DIRECT_INPUT)!= True) and (oExecutedInstruction.testdata != "")):
            oDataDriver = DataDriver(oExecutedInstruction.testdata)
            oExecutedInstruction.set_testdata_detailed(oDataDriver)

        # update the existing object with pre-dependency information
        self.instructionsDict[sInstructionName] = oExecutedInstruction

    #=============================================================================#
    # Method: EvaluatePostDependency(self,oException)
    # Description: Evaluates the post dependecies of the provided instruction
    #=============================================================================#
    def EvaluatePostDependency(self,oExecutedInstruction,bTakeScreenshot):
        # if expected result matches actual result, then change status to success
        Logger.note.debug("Evaluting Post Dependency")

        if oExecutedInstruction.expectedresult == oExecutedInstruction.actualresult:
            #Logger.note.debug("Sucess: Updated Status")
            oExecutedInstruction.status = Constants.STATUS_SUCCESS
        else:
            Logger.note.debug("Expected result do not match actuals. Screenshot may be attached")
            if bTakeScreenshot == True:
                sLabel = oExecutedInstruction.label
                oFrame = stbt.get_frame()
                cv2.imwrite(sLabel+".png",oFrame)

            # update status of the executed instruction
            # if no screenshot is needed, its a skipped instruction
            if bTakeScreenshot == False:
                oExecutedInstruction.status = Constants.STATUS_SKIPPED
            else:
                oExecutedInstruction.status = Constants.STATUS_FAILURE

            # if exit test case on error, raise appropriate exception
            if oExecutedInstruction.options_detailed.has_key(Constants.EXIT_TC_ON_ERROR):
                raise CustomException(Constants.EXIT_TC_ON_ERROR)
            # if exit test case, raise appropriate exception
            elif(oExecutedInstruction.options_detailed.has_key(Constants.EXIT_ON_ERROR)):
                raise CustomException(Constants.EXIT_ON_ERROR)

class MessageManager:
    """
    Common Functions required for managing messages

    Args:
        oInstruction: an instruction object with keyword, its respected expected result,
        option and its data

    """
    def __init__(self,sLabel,sDelimiter=Constants.DELIMITER_PIPE):
        """
        Initializes the MessageManager class with information required provided information

        Args:
            sLabel: Label the message type
            sDetails: add details for provided label

        Returns:
            Nothing

        Raises:
            Nothing
        """
        self.label = sLabel
        self.delimiter = sDelimiter
        self.details = collections.OrderedDict()
        Logger.note.debug("Created a new message manager with Name <%s>" % self.label)

    def Add(self,sLabelName,sDetails):
        """
        Adds the provided message in provided MM

        Args:
            sDetails: add details on the existing message manager

        Returns:
            Nothing

        Raises:
            Nothing
        """
        if sDetails != None:
            if sLabelName in self.details:
                sExistingValue = self.details[sLabelName]
                sNewValue = sExistingValue + Constants.DELIMITER_SEMICOLON + sDetails
                self.details[sLabelName] = sNewValue
            else:
                self.details[sLabelName] = sDetails
        Logger.note.debug("Added message <%s> to label <%s>" % (sDetails,sLabelName))

    def Message(self):
        """
        Provides the message with new line seperator for each message

        Returns:
            the complete constructed message in message manager
        """
        #sReturnString = ""
        #sReturnString = self.delimiter.join(['{}'.format(sValue) for sValue in self.details.values()])
        #Logger.note.debug("Complete Message: <%s>" % sReturnString)
        #return sReturnString
        return self.details
