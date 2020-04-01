#  @file InputTest.py
#  @author Nicholas Mari
#  @brief Tests functionality of Input.py
#  @date 03/24/2020

from os import curdir, path
import sys

from inspect import currentframe, getfile
from pytest import fixture, raises

current_dir = path.dirname(path.abspath(getfile(currentframe())))
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Input import *

class TestKeywordFromFile:

	def test_no_params(self):

		args = keywordFromFile(".\\ConfigForTesting\\noParams.txt")

		assert args == {
							"keyword" : "Default",
							"limit" : 10,
							"safesearch" : False,
							"directory" : ".\\Images",
							"filetype" : "",
							"colour" : "",
							"license" : "",
							"imageage" : "",
							"imagetype" : "",
							"aspectratio" : "",
							"imagesize" : "",
							"serverhost" : "",
							"serverusername" : "",
							"serverpassword" : "",
							"whitelist": "",
							"region" : "",
							"blacklist": ""
						}

	def test_all_params(self):

		args = keywordFromFile(".\\ConfigForTesting\\allParams.txt")

		assert args == {
							"keyword" : "Default",
							"limit" : 10,
							"safesearch" : True,
							"directory" : ".\\Images",
							"filetype" : "jpg",
							"colour" : "red",
							"license" : "labeled-for-noncommercial-reuse-with-modification",
							"imageage" : "past-7-days",
							"imagetype" : "photo",
							"aspectratio" : "wide",
							"imagesize" : "medium",
							"serverhost" : "",
							"serverusername" : "",
							"serverpassword" : "",
							"whitelist": ".edu",
							"region" : "Greece",
							"blacklist" : "wikipedia.ca"
						}

	def test_invalid_file(self):

		with raises(Exception):
			assert keywordFromFile(".\\ConfigForTesting\\noFile.txt")

	def test_no_keyword(self):
		with raises(Exception):
			assert keywordFromFile('.\\ConfigForTesting\\noKeyword.txt')

	def test_all_missing_but_keyword(self):
		args = keywordFromFile('.\\ConfigForTesting\\nothingButKeyword.txt')

		assert args == {
							"keyword" : "default",
							"limit" : 10,
							"safesearch" : False,
							"directory" : ".\\Images",
							"filetype" : "",
							"colour" : "",
							"license" : "",
							"imageage" : "",
							"imagetype" : "",
							"aspectratio" : "",
							"imagesize" : "",
							"serverhost" : "",
							"serverusername" : "",
							"serverpassword" : "",
							"whitelist": "",
							"region" : "",
							"blacklist": ""
						}
				