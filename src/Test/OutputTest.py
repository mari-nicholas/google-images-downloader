## @file OutputTest.py
#  @author Samuel Crawford
#  @brief Tests the functionality of Output.pt
#  @date 03/25/2020

from os import curdir, chdir, path, rmdir
import sys

from inspect import currentframe, getfile
from pytest import fixture, raises

current_dir = path.dirname(path.abspath(getfile(currentframe())))
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Output import *

class TestCreateDir:
    def test_exist_directory(self, capfd):
        newPath = path.join(curdir, "Images")
        assert path.isdir(newPath)

        createDir(curdir, "Images")
        out, err = capfd.readouterr()

        assert out == "Directory Images already exists\n"
        assert path.isdir(newPath)

    def test_error_creating_directory(self, capfd):
        newPath = path.join(curdir, "nonexistant")
        assert not path.isdir(newPath)

        createDir(newPath, "Images")
        out, err = capfd.readouterr()

        assert out == "Creation of the directory Images failed\n"
        assert not path.isdir(newPath)
        assert not path.isdir(path.join(newPath, "Images"))

    def test_success_creating_directory(self, capfd):
        newPath = path.join(curdir, "Images", "test")
        assert not path.isdir(newPath)

        createDir(path.join(curdir, "Images"), "test")
        out, err = capfd.readouterr()

        assert out == "Successfully created the directory test\n"
        assert path.isdir(newPath)
        rmdir(newPath)
        assert not path.isdir(newPath)

# local function for comparing data read from request to data read from saved image
def imageEqualsRequest(url, filename):
    with open(path.join(curdir, "ImagesForTesting", filename), "rb") as f:
        saved = f.read()

    return saved == getRequest(url)

class TestGetRequest:
    def test_JPG(self, capfd):
        assert imageEqualsRequest("https://pbs.twimg.com/profile_images/1162710956218245120/L4b1guuv_400x400.jpg", "cursed.jpg")

    def test_GIF(self, capfd):
        assert imageEqualsRequest("https://www.homestuck.com/images/storyfiles/hs2/00379.gif", "youthRoll.gif")

    def test_PNG(self, capfd):
        assert imageEqualsRequest("https://www.kindpng.com/picc/m/198-1985747_pillow-clipart-neat-sonic-body-pillow-hd-png.png", "sonic.png")
