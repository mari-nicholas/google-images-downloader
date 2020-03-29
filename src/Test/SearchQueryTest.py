## @file SearchQueryTest.py
#  @author Nicholas Mari
#  @brief Tests the functionality of SearchQuery.py
#  @date 03/28/2020

from os import path
import sys

from inspect import currentframe, getfile
from pytest import fixture, raises

current_dir = path.dirname(path.abspath(getfile(currentframe())))
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from SearchQuery import *

class TestBuildURLParam:

	def test_no_params(self):

		args = {
					"filetype" : "",
					"colour" : "",
					"license" : "",
					"imagetype" : "",
					"imageage" : "",
					"aspectratio" : "",
					"imagesize" : ""
				}

		params = buildURLParam(args)

		print(params)

		assert params == ''

	def test_all_params(self):
		args = {
					"filetype" : "jpg",
					"colour" : "red",
					"license" : "labeled-for-noncommercial-reuse-with-modification",
					"imagetype" : "photo",
					"imageage" : "past-7-days",
					"aspectratio" : "wide",
					"imagesize" : "medium"
				}

		params = buildURLParam(args)

		assert params == 'iar:w,ic:specific,isc:red,ift:jpg,qdr:w,isz:m,itp:photo,sur:fm'
