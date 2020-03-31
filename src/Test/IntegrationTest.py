## @file IntegrationTest.py
#  @author Joshua Guinness
#  @brief Test the integration between modules
#  @date 03/31/2020

from os import curdir, chdir, path, remove, rmdir
import sys

from inspect import currentframe, getfile
from pytest import fixture, raises
import re

current_dir = path.dirname(path.abspath(getfile(currentframe())))
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Input import *
from Main import *
from Output import *
from SearchQuery import *
from NavigatePage import *

args = {
			"keyword" : "default",
			"limit" : 5,
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
			"serverpassword" : ""
		}

searchURL = 'https://www.google.com/search?q=' + 'default' + \
    '&tbm=isch&hl=en&hl=en&tbs=' + quote('iar:w,ic:specific,isc:red,ift:jpg,qdr:w,isz:m,itp:photo,sur:fm'.encode('utf-8')) + \
    '&ved=0CAMQ2J8EahcKEwjgteiDqrToAhUAAAAAHQAAAAAQAg&biw=1519&bih=760&safe=active'

def test_input_to_searchquery():

    url = buildURL(args)
    assert url == searchURL

def test_searchquery_to_navigatepage():

    url = buildURL(args)
    urls = getImageURL(url, args["limit"])
    assert len(urls) == 5

    for i in urls:
        result = re.match("http.", i)
        assert result != None
