## @file SystemTest.py
#  @author Joshua Guinness
#  @brief System level automated functional tests as descirbed in our test plan
#  @date 04/03/2020

from os import curdir, chdir, path, remove, rmdir, listdir, fsencode, fsdecode, mkdir
import sys
from shutil import rmtree

from inspect import currentframe, getfile
from PIL import Image
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

args1 = {
			"keyword": "default",
			"limit": 3,
			"safesearch": True,
			"directory": path.join(curdir, "Images"),
			"filetype": "gif",
			"colour": "",
			"license": "",
			"imagetype": "",
			"imageage": "",
			"aspectratio": "",
			"imagesize": "",
			"serverhost": "",
			"serverusername": "",
			"serverpassword": "",
			"whitelist": "",
            "blacklist": "",
			"region": ""
		}

args2 = {
			"keyword": "mcmaster engineering",
			"limit": 3,
			"safesearch": True,
			"directory": path.join(curdir, "Images"),
			"filetype": "",
			"colour": "",
			"license": "",
			"imagetype": "",
			"imageage": "",
			"aspectratio": "",
			"imagesize": "",
			"serverhost": "",
			"serverusername": "",
			"serverpassword": "",
			"whitelist": "",
            "blacklist": "mcmaster.ca",
			"region": ""
		}

args3 = {
			"keyword": "engineering",
			"limit": 3,
			"safesearch": True,
			"directory": path.join(curdir, "Images"),
			"filetype": "",
			"colour": "",
			"license": "",
			"imagetype": "",
			"imageage": "",
			"aspectratio": "",
			"imagesize": "",
			"serverhost": "",
			"serverusername": "",
			"serverpassword": "",
			"whitelist": "mcmaster.ca",
            "blacklist": "",
			"region": ""
		}

args4 = {
			"keyword": "software",
			"limit": 40,
			"safesearch": True,
			"directory": path.join(curdir, "Images"),
			"filetype": "",
			"colour": "",
			"license": "",
			"imagetype": "",
			"imageage": "",
			"aspectratio": "",
			"imagesize": "",
			"serverhost": "",
			"serverusername": "",
			"serverpassword": "",
			"whitelist": "",
            "blacklist": "",
			"region": ""
		}

args5 = {
			"keyword": "software",
			"limit": 2,
			"safesearch": True,
			"directory": path.join(curdir, "newDirec"),
			"filetype": "",
			"colour": "",
			"license": "",
			"imagetype": "",
			"imageage": "",
			"aspectratio": "",
			"imagesize": "",
			"serverhost": "",
			"serverusername": "",
			"serverpassword": "",
			"whitelist": "",
            "blacklist": "",
			"region": ""
		}

args6 = {
            "keyword": "homestuck",
            "limit": 5,
            "safesearch": True,
            "directory": path.join(curdir, "Images"),
            "filetype": "jpg",
            "colour": "",
            "license": "",
            "imagetype": "",
            "imageage": "",
            "aspectratio": "",
            "imagesize": ">2MP",
            "serverhost": "",
            "serverusername": "",
            "serverpassword": "",
            "whitelist": "",
            "blacklist": "",
            "region": ""
        }

args7 = {
            "keyword": "homestuck",
            "limit": 5,
            "safesearch": True,
            "directory": "",
            "filetype": "gif",
            "colour": "green",
            "license": "",
            "imagetype": "",
            "imageage": "",
            "aspectratio": "",
            "imagesize": "",
            "serverhost": "",
            "serverusername": "",
            "serverpassword": "",
            "whitelist": "",
            "blacklist": "",
            "region": "Canada"
        }


class TestSearchQueries:
    #FR-SQ2
    def test_specific_file_type(self, delete_args1_folder):
        url = buildURL(args1)
        urls = getImageURL(url, args1["limit"], args1['blacklist'])
        downloadImages(urls, args1["keyword"], args1["directory"])
        
        directory = fsencode(path.join(curdir, "Images", args1["keyword"]))

        for file in listdir(directory):
            filename = fsdecode(file)
            assert filename.endswith(".gif")


    @fixture()
    def delete_args1_folder(self):
        yield TestSearchQueries.delete_args1_folder
        rmtree(path.join(curdir, "Images", args1["keyword"]))


    #FR-SQ3
    def test_blacklist_site(self):
        url = buildURL(args2)
        urls = getImageURL(url, args2["limit"], args2['blacklist'])
        
        for site in urls:
            result = re.search("mcmaster.ca", site)
            assert result == None


    #FR-SQ4
    def test_whitelist_site(self):
        url = buildURL(args3)
        urls = getImageURL(url, args3["limit"], args3['blacklist'])
        
        for site in urls:
            result = re.search("mcmaster.ca", site)
            assert result != None

    #FR-SQ5
    def test_file_size(self, delete_args6_folder):
        url = buildURL(args6)
        urls = getImageURL(url, args6["limit"], args6['blacklist'])
        downloadImages(urls, args6["keyword"], args6["directory"])
        
        directory = path.join(curdir, "Images", args6["keyword"])
        
        for file in listdir(directory):
            image = Image.open(path.join(directory, file))
            width, height = image.size
            assert width * height > 2000000 * 0.9 # tolerance for issues on Google's end

    @fixture()
    def delete_args6_folder(self):
        yield TestSearchQueries.delete_args6_folder
        rmtree(path.join(curdir, "Images", args6["keyword"]))

    #FR-SQ6
    def test_blacklist_site(self):
        url = buildURL(args7)
        urls = getImageURL(url, args7["limit"], args7['blacklist'])

        fileArgs = keywordFromFile(path.join(curdir, "Test", "ConfigForTesting", "homestuckFile.txt"))
        fileUrl = buildURL(fileArgs)
        fileUrls = getImageURL(url, fileArgs["limit"], fileArgs['blacklist'])

        assert set(urls) == set(fileUrls)


class TestDownloadImages:


    #FR-DL1
    def test_correct_number_images_downloaded(self, delete_args4_folder):
        url = buildURL(args4)
        urls = getImageURL(url, args4["limit"], args4['blacklist'])
        downloadImages(urls, args4["keyword"], args4["directory"])
        
        directory = fsencode(path.join(curdir, "Images", args4["keyword"]))
        number = 0

        for file in listdir(directory):
            number += 1
        
        assert number <= args4["limit"]


    @fixture()
    def delete_args4_folder(self):
        yield TestDownloadImages.delete_args4_folder
        rmtree(path.join(curdir, "Images", args4["keyword"]))


    #FR-DL2
    def test_specified_directory(self, specified_directory):
        url = buildURL(args5)
        urls = getImageURL(url, args5["limit"], args5['blacklist'])
        downloadImages(urls, args5["keyword"], args5["directory"])

        directory = fsencode(path.join(args5["directory"], args5["keyword"]))
        number = 0

        for file in listdir(directory):
            number += 1
        
        assert number == args5["limit"]


    @fixture()
    def specified_directory(self):
        mkdir(args5["directory"])
        yield TestDownloadImages.specified_directory
        rmtree(args5["directory"])