## @file SearchQueryTest.py
#  @author Nicholas Mari
#  @brief Tests the functionality of SearchQuery.py
#  @date 03/28/2020

from os import curdir, path
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
					"keyword" : "default",
					"limit" : 10,
					"safesearch" : False,
					"directory" : path.join(curdir, "Images"),
					"filetype" : "",
					"colour" : "",
					"license" : "",
					"imagetype" : "",
					"imageage" : "",
					"aspectratio" : "",
					"imagesize" : "",
					"serverhost" : "",
					"serverusername" : "",
					"serverpassword" : "",
					"whitelist": "",
					"region" : ""
				}

		params = buildURLParam(args)

		assert params == ''

	def test_all_params(self):
		args = {
					"keyword" : "default",
					"limit" : 10,
					"safesearch" : False,
					"directory" : path.join(curdir, "Images"),
					"filetype" : "jpg",
					"colour" : "red",
					"license" : "labeled-for-noncommercial-reuse-with-modification",
					"imagetype" : "photo",
					"imageage" : "past-7-days",
					"aspectratio" : "wide",
					"imagesize" : "medium",
					"serverhost" : "",
					"serverusername" : "",
					"serverpassword" : "",
					"whitelist": "",
					"region" : ""
				}

		params = buildURLParam(args)

		assert params == 'iar:w,ic:specific,isc:red,ift:jpg,qdr:w,isz:m,itp:photo,sur:fm'

class TestBuildURL:

	def test_no_params(self):
		args = {
					"keyword" : "default",
					"limit" : 10,
					"safesearch" : False,
					"filetype" : "",
					"directory" : "",
					"colour" : "",
					"colourtype" : "",
					"license" : "",
					"imagetype" : "",
					"imageage" : "",
					"aspectratio" : "",
					"imagesize" : "",
					"serverhost" : "",
					"serverusername" : "",
					"serverpassword" : "",
					"whitelist": "",
					"region" : ""
				}

		url = buildURL(args)

		assert url == 'https://www.google.com/search?as_st=y&tbm=isch&hl=en' + \
    				'&as_q=' + 'default' + '&as_epq=&as_oq=&as_eq='+ \
    				'&cr='+ '' +\
    				'&as_sitesearch=' + '' + \
    				'&tbs='+ '' +\
    				'&safe=images'


	def test_all_params(self):
		args = {
					"keyword" : "default",
					"limit" : 10,
					"safesearch" : True,
					"directory" : path.join(curdir, "Images"),
					"filetype" : "jpg",
					"colour" : "red",
					"license" : "labeled-for-noncommercial-reuse-with-modification",
					"imagetype" : "photo",
					"imageage" : "past-7-days",
					"aspectratio" : "wide",
					"imagesize" : "medium",
					"serverhost" : "",
					"serverusername" : "",
					"serverpassword" : "",
					"whitelist": ".edu",
					"region" : "Greece"
				}

		url = buildURL(args)

		assert url == 'https://www.google.com/search?as_st=y&tbm=isch&hl=en' + \
    				'&as_q=' + 'default' + '&as_epq=&as_oq=&as_eq='+ \
    				'&cr='+ 'countryGR' +\
    				'&as_sitesearch=' + quote('.edu'.encode('utf-8')) + \
    				'&tbs='+ quote('iar:w,ic:specific,isc:red,ift:jpg,qdr:w,isz:m,itp:photo,sur:fm'.encode('utf-8')) +\
    				'&safe=active'
