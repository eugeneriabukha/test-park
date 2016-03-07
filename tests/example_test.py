from time import sleep
import stbt
import os

from scripts.Constants import *
from scripts.DataDriver import *
from scripts.CustomException import *
from scripts.KeywordDriver import *
from scripts.KeywordFactory import *

def test_able_to_send_commands():
    stbt.press('KEY_MENU')  # Close any open menus
    assert stbt.wait_for_motion()

def test_that_live_tv_is_playing():
    stbt.press('KEY_CLOSE')  # Close any open menus
    assert stbt.wait_for_motion()

def test_that_stb_tester_logo_is_shown():
    stbt.press('KEY_CHANNELUP')
    assert stbt.wait_for_match('stb-tester-logo.png')

def test_read_menu():
    stbt.press('KEY_CLOSE')
    sleep(1)
    stbt.press('KEY_MENU')
    sleep(1)
    print stbt.ocr()

def test_run_keyworddriver():
    # Create an Object for DataDriver
    print Constants.TESTCASE_START
    oDataDriver = DataDriver("Instructions_RealTest.xls:Instructions")
    oKeywordDriver = KeywordDriver(oDataDriver)
    # Starts the Exectution of the instuction set
    oKeywordDriver.Execute()
