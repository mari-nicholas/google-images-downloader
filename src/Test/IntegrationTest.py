## @file IntegrationTest.py
#  @author Joshua Guinness
#  @brief Test the integration between modules
#  @date 03/31/2020

from os import curdir, chdir, path, remove, rmdir
import sys
import os

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
			"serverpassword" : "",
			"whitelist": "",
			"region" : ""
		}

searchURL = 'https://www.google.com/search?as_st=y&tbm=isch&hl=en' + \
    '&as_q=' + 'default' + '&as_epq=&as_oq=&as_eq='+ \
    '&cr='+ '' +\
    '&as_sitesearch=' + '' + \
    '&tbs='+ quote('iar:w,ic:specific,isc:red,ift:jpg,qdr:w,isz:m,itp:photo,sur:fm'.encode('utf-8')) + \
    '&safe=active'

listOfURLs = ["https://cdn.mos.cms.futurecdn.net/6h8C6ygTdR2jyyUxkALwsc-1200-80.jpg", 
"https://1fdj2e2egv3mhacyt2xo9f01-wpengine.netdna-ssl.com/wp-content/uploads/2019/04/16288974_web1_190410-SAA-Mammoth-Donkeys_2.jpg",
"https://www.aspcapro.org/sites/default/files/styles/image_component/public/page/card/image/donkeynose.jpg?itok=s7-KmNux",
"https://scx1.b-cdn.net/csz/news/800/2019/donkey.jpg",
"https://media.npr.org/assets/img/2019/04/24/gettyimages-942051048-29251d02758b345d0e722ef87f412b13cc19a265-s800-c85.jpg"]

def test_input_to_searchquery():

    url = buildURL(args)
    assert url == searchURL

def test_searchquery_to_navigatepage():

    url = buildURL(args)
    urls = getImageURL(url, args["limit"], "")
    assert len(urls) == 5

    for i in urls:
        result = re.match("http.", i)
        assert result != None

def test_navigatepage_to_output(delete_image_folder):
    downloadImages(listOfURLs, "donkeys", path.join(curdir, 'Images'))
    assert os.path.isdir("Images/donkeys")

@pytest.fixture()
def delete_image_folder():
    yield delete_image_folder
    chdir("Images")
    rmtree("donkeys")