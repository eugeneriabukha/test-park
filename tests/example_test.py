from time import sleep
import stbt

import os
dir = os.path.dirname(__file__)
print dir
filename = os.path.join(dir, '/shared/scripts/KeywordDriver.py')
print filename
import filename


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
    print "x"
