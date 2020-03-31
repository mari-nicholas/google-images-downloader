## @file NavigatePageTest.py
#  @author Joshua Guinness
#  @brief Tests the functionality of NavigatePage.py
#  @date 03/25/2020

from os import curdir, chdir, path, remove, rmdir
import sys
import re

from inspect import currentframe, getfile
from pytest import fixture, raises

current_dir = path.dirname(path.abspath(getfile(currentframe())))
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from NavigatePage import *

donkeysURL = "https://www.google.com/search?q=donkeys\
    &tbm=isch&ved=2ahUKEwjo7fam_rvoAhUS96wKHRdrDhkQ2-\
        cCegQIABAA&oq=donkeys&gs_lcp=CgNpbWcQAzIECCMQ\
            JzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyA\
                ggAMgIIADoECAAQQ1DFlgNYsJwDYJSdA2gAcA\
                    B4AIABUYgB_AOSAQE3mAEAoAEBqgELZ3d\
                        zLXdpei1pbWc&sclient=img&ei=M\
                            aR-XqiRBJLuswWX1rnIAQ&bih\
                                =1344&biw=1183"

mcmasterURL = "https://www.google.com/search?q=mcmaster\
    &tbm=isch&ved=2ahUKEwjd4YGg_bvoAhUGbqwKHXIyAAMQ2-cC\
        egQIABAA&oq=mcmaster&gs_lcp=CgNpbWcQAzICCAAyAgg\
            AMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCA\
                A6BAgjECc6BAgAEENQ7I4RWPCXEWC3mRFoAHAAe\
                    ACAAY0BiAHkBZIBAzUuM5gBAKABAaoBC2d3\
                        cy13aXotaW1n&sclient=img&ei=FqN\
                            -Xt3-B4bcsQXy5IAY&bih=1344&\
                                biw=1183"

softwareURL = "https://www.google.com/search?q=software\
    &tbm=isch&ved=2ahUKEwi61tfA_rvoAhUKDq0KHfP2D24Q2-cC\
        egQIABAA&oq=software&gs_lcp=CgNpbWcQAzIECCMQJzI\
            ECCMQJzICCAAyAggAMgIIADICCAAyAggAMgIIADICCA\
                AyAggAOgQIABBDOgUIABCDAVCp5wVYl_AFYPvwB\
                    WgAcAB4AIABWogB5gSSAQE4mAEAoAEBqgEL\
                        Z3dzLXdpei1pbWc&sclient=img&ei=\
                            Z6R-XvqGBYqctAXz7b_wBg&bih=\
                                1344&biw=1183"

def test_donkeys():
    urlList = getImageURL(donkeysURL, 5)
    assert len(urlList) == 5


def test_monkeys():
    urlList = getImageURL(mcmasterURL, 5)
    assert len(urlList) == 5


def test_software():
    urlList = getImageURL(softwareURL, 5)
    assert len(urlList) == 5


def test_correct_number_large_urls():
    urlList = getImageURL(donkeysURL, 40)
    assert len(urlList) == 40


def test_list_contains_urls():
    urlList = getImageURL(mcmasterURL, 10)
    for i in urlList:
        result = re.match("http.", i)
        assert result != None


def test_improper_input():
    with pytest.raises(ValueError):
        urlList = getImageURL(mcmasterURL, -5)