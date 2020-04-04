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

class TestUserInput:

	def test_nothing_but_keyword(self):
		sys.argv = ['Main.py', '-k', 'test']
		args = userInput()

		assert args == {
							"keyword" : "test",
							"limit" : 10,
							"safesearch" : False,
							"directory" : path.join(curdir, 'Images'),
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

	def test_from_file(self):
		sys.argv = ['Main.py', '-ff', path.join(curdir, 'Test', 'ConfigForTesting', 'allParams.txt')]

		args = userInput()

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

	def test_all_args(self):
		sys.argv = ['Main.py', '-k', 'Default', '-l', '10', '-ss', '-d', '.\\Images', '-ft', 'jpg', '-c', 'red', '-li', 'labeled-for-noncommercial-reuse-with-modification', '-a', 'past-7-days', '-t', 'photo', '-ar', 'wide', '-is', 'medium', '-s', 'moore.mcmaster.ca', '-u', 'marin', '-p', 'no', '-wl', '.edu', '-rg', 'Greece', '-bl', 'wikipedia.ca']
		args = userInput()

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
							"serverhost" : "moore.mcmaster.ca",
							"serverusername" : "marin",
							"serverpassword" : "no",
							"whitelist": ".edu",
							"region" : "Greece",
							"blacklist" : "wikipedia.ca"
						}

class TestKeywordFromFile:

	def test_no_params(self):

		args = keywordFromFile(path.join(curdir, 'Test', 'ConfigForTesting', 'noParams.txt'))

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

		args = keywordFromFile(path.join(curdir, 'Test', 'ConfigForTesting', 'allParams.txt'))

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
			assert keywordFromFile(path.join(curdir, 'Test', 'ConfigForTesting', 'noFile.txt'))

	def test_no_keyword(self):
		with raises(Exception):
			assert keywordFromFile(path.join(curdir, 'Test', 'ConfigForTesting', 'noKeyword.txt'))

	def test_all_missing_but_keyword(self):
		args = keywordFromFile(path.join(curdir, 'Test', 'ConfigForTesting', 'nothingButKeyword.txt'))

		assert args == {
							"keyword" : "default",
							"limit" : 10,
							"safesearch" : False,
							"directory" : path.join(curdir, 'Images'),
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
