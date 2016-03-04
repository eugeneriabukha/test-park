from Constants import Constants
from CustomException import CustomException
import os
import xlrd
#=============================================================================#
# File: DataDriver.py
#
#  Copyright (c) 2016, Prithvi Nath Manikonda, Vinoth Kumar Ravichandran
#  All rights reserved.
#
# Description: Functions and methods for Data Driver Scripts
#    These functions and methods are application and platform independent, and
#    are NOT specific to Web based applications.
#
# Modules:
#
# Classes Added or Extended:
#    DataDriver
#
#
#=============================================================================#

#=============================================================================#
# Require and Include section
# Entries for additional files or methods needed by these methods
#=============================================================================#
#Constants
#xlrd

#=============================================================================#
# Class: DataDriver
#=============================================================================#

class DataDriver(dict):
    #=============================================================================#
    # Method: __init__(self,fileName_Rows)
    # Description:
    # Variables: fileName_Rows: this input combines 3 varied inputs due to limitations
    #               sub input 1: fileName : xls file name to work with
    #               sub input 2: sheetName: name of the xls sheet to work on
    #               sub input 3: rowsNumbers: row numbers in the sheet to fetch
    #
    # Input samples: Instructions.xls:Instructions:1,3-5,7
    #               the above input would fetch rows 1,3,4,5,7th row from Instructions sheet
    # of Instructions.xls file.
    #       sample2: Instructions.xls:Login
    #           fetches all rows of login sheet of Instructions.xls
    # Returns:
    # Usage Examples:
    #
    #=============================================================================#
    def __init__(self,fileName_Rows):
        # fetch the input and split it to an array by seperator colon
        arfileName = fileName_Rows.split(Constants.DELIMITER_COLON)
        fileName = ""
        sRowAnalyzer = ""
        arRows = list()

        # decide on the scenario based on the number of inputs provided
        if len(arfileName) == 3:
          fileName = arfileName[0]
          fSheetName = arfileName[1]
          sRowAnalyzer = arfileName[2]
          # fetch the list of rows which has to be fetched
          arRows = self.RowAnalyzer(sRowAnalyzer)
        elif len(arfileName) == 2:
          fileName = arfileName[0]
          fSheetName = arfileName[1]
        else:
            try:
                # Raise an exception with argument
                raise CustomException("Too Few Parameters")
            except CustomException, arg:
                # Catch the custom exception
                print 'Error: ', arg.name

        # find the current path of the data file
        #sPath = str(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))+"/data/"
        sPath = os.path.dirname(os.path.realpath(__file__))
        sPath = str(sPath)
        sPath.replace("scripts","data")
        #sPath = sPath + "/data/"
        sPath = sPath + str(fileName)
        if not (os.path.exists(sPath)):
            try:
                # Raise an exception with argument
                raise CustomException("File do NOT exist : Path <#%s> : File Name <#%s>" %(sPath,fileName))
            except CustomException, arg:
                # Catch the custom exception
                print 'Error: ', arg.name


        # Fetch the column headers for later usage
        arFieldNames = list()
        xlWorkbook = xlrd.open_workbook(sPath)
        xlSheet = xlWorkbook.sheet_by_name(fSheetName)
        for rowNumber in range(0, xlSheet.nrows):
            arLabel = xlSheet.row_values(rowNumber)
            arFieldNames = (arLabel)
            break

        # fetch all the other rows and add it to a dictionary with headers as keys and cell values as value
        iCounter = 1
        hReturn = dict()
        for rowNumber in range(1, xlSheet.nrows):
            hInside = dict()
            for sFieldName in range(0,len(arFieldNames)):
                arLabel = xlSheet.cell(rowNumber,sFieldName).value
                hInside[arFieldNames[sFieldName]] = arLabel
            hReturn[iCounter] = hInside
            iCounter = iCounter + 1

        # quit if expected number of rows to be fetched greater than the actual rows in the excel
        if len(arRows) > len(hReturn):
            try:
                # Raise an exception with argument
                raise CustomException("Array length <%d> cannot be greater than requested row count <%d>" %(len(hReturn),len(arRows)))
            except CustomException, arg:
                # Catch the custom exception
                print 'Error: ', arg.name


        # if specific rows are requested, provide them else provide the complete list of rows fetched
        if sRowAnalyzer != "":
            for i in arRows:
                if bool(hReturn[i]):
                    self[i] = hReturn[i]
                else:
                    try:
                        # Raise an exception with argument
                        raise CustomException("RowNumber [#%s] was not available in the excel sheet [#%s]" %(rowID,fileName))
                    except CustomException, arg:
                        # Catch the custom exception
                        print 'Error: ', arg.name
        else:
            self.update(hReturn)

    #=============================================================================#
    # Method: RowAnalyzer(self,sRowInfo)
    # Description:
    # Returns:
    # Usage Examples:
    #=============================================================================#
    def RowAnalyzer(self,sRowInfo):
        arRow = list()
        # split the provided input with commas to fetch the different row set
        arRowInfo = sRowInfo.split(Constants.DELIMITER_COMMA)
        # for each row set, find out if its a single row or multiple and process accordingly
        for sRow in arRowInfo:
            arRowSplit = sRow.split(Constants.DELIMITER_HIFEN)
            arRowSplit=[int(i) for i in arRowSplit]
            # only when there is a hifen, you get two results
            if (len(arRowSplit) == 2):
                for iCounter in range(arRowSplit[0],arRowSplit[1]+1):
                    arRow.append(iCounter)
            elif len(arRowSplit) == 1:
                arRow.append(arRowSplit[0])
        return arRow

    #=============================================================================#
    # End Of Class: DataDriver
    #=============================================================================#
