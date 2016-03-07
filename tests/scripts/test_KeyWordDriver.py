from KeywordDriver import KeywordDriver
from DataDriver import DataDriver
import time
# Test Case to check the operation of KeywordDriver Class
# Create an Object for DataDriver
oDataDriver = DataDriver("Instructions_Login.xls:Instructions")
oKeywordDriver = KeywordDriver(oDataDriver)
# Starts the Exectution of the instuction set
oKeywordDriver.Execute()
