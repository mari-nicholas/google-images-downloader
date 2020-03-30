## @file OutputTest.py
#  @author Samuel Crawford
#  @brief Tests the functionality of Output.py
#  @date 03/25/2020

from os import curdir, chdir, path, remove, rmdir
import sys

from inspect import currentframe, getfile
# from pytest import fixture, raises
import pytest

current_dir = path.dirname(path.abspath(getfile(currentframe())))
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Output import *

class TestCreateDir:
    def test_exist_directory(self, capfd):
        newDir = path.join(curdir, "Images")
        assert path.isdir(newDir)

        createDir(newDir)
        out, err = capfd.readouterr()

        assert out == "Directory " + newDir + " already exists\n"
        assert path.isdir(newDir)

    def test_error_creating_directory(self, capfd):
        parDir = path.join(curdir, "nonexistant")
        newDir = path.join(parDir, "Images")
        assert not path.isdir(newDir)

        createDir(newDir)
        out, err = capfd.readouterr()

        assert out == "Creation of the directory " + newDir + " failed\n"
        assert not path.isdir(parDir)
        assert not path.isdir(newDir)

    def test_success_creating_directory(self, capfd):
        newDir = path.join(curdir, "Images", "test")
        assert not path.isdir(newDir)

        createDir(newDir)
        out, err = capfd.readouterr()

        assert out == "Successfully created the directory " + newDir + "\n"
        assert path.isdir(newDir)
        rmdir(newDir)
        assert not path.isdir(newDir)

# local function for comparing data read from request to data read from saved image
def imageEqualsRequest(url, filename):
    with open(path.join(curdir, "Test", "ImagesForTesting", filename), "rb") as f:
        saved = f.read()

    return saved == getRequest(url)

class TestGetRequest:
    def test_JPG(self, capfd):
        assert imageEqualsRequest("https://pbs.twimg.com/profile_images/1162710956218245120/L4b1guuv_400x400.jpg", "cursed.jpg")

    def test_GIF(self, capfd):
        assert imageEqualsRequest("https://www.homestuck.com/images/storyfiles/hs2/00379.gif", "youthRoll.gif")

    def test_PNG(self, capfd):
        assert imageEqualsRequest("https://www.kindpng.com/picc/m/198-1985747_pillow-clipart-neat-sonic-body-pillow-hd-png.png", "sonic.png")

# local function for comparing data read from two saved images
def imageEqualsImage(testFile, d, img):
    with open(path.join(curdir, "Test", "ImagesForTesting", testFile), "rb") as f:
        img1 = f.read()

    with open(path.join(d, img), "rb") as f:
        img2 = f.read()

    return img1 == img2


class TestDownloadImages:
    def test_normal(self, capfd):
        downloadDir = path.join(curdir, "Images", "testing")
        assert not path.isdir(downloadDir)

        downloadImages(["https://pbs.twimg.com/profile_images/1162710956218245120/L4b1guuv_400x400.jpg",
            "https://www.homestuck.com/images/storyfiles/hs2/00379.gif",
            "https://www.kindpng.com/picc/m/198-1985747_pillow-clipart-neat-sonic-body-pillow-hd-png.png"],
            "testing", path.join(curdir, "Images"))

        assert path.isdir(downloadDir)
        assert imageEqualsImage("cursed.jpg", downloadDir, "testing0.jpg")
        assert imageEqualsImage("youthRoll.gif", downloadDir, "testing1.gif")
        assert imageEqualsImage("sonic.png", downloadDir, "testing2.png")

        remove(path.join(downloadDir, "testing0.jpg"))
        remove(path.join(downloadDir, "testing1.gif"))
        remove(path.join(downloadDir, "testing2.png"))
        rmdir(downloadDir)

        assert not path.isdir(downloadDir)

        out, err = capfd.readouterr()
        assert out == """Successfully created the directory .\\Images\\testing

Getting image from: https://pbs.twimg.com/profile_images/1162710956218245120/L4b1guuv_400x400.jpg
\033[0;32mImage downloaded\033[0m

Getting image from: https://www.homestuck.com/images/storyfiles/hs2/00379.gif
\033[0;32mImage downloaded\033[0m

Getting image from: https://www.kindpng.com/picc/m/198-1985747_pillow-clipart-neat-sonic-body-pillow-hd-png.png
\033[0;32mImage downloaded\033[0m
"""

    def test_base64(self, capfd):
        downloadDir = path.join(curdir, "Images", "testing")
        #assert not path.isdir(downloadDir)

        #get base64 data from file
        with open(path.join(curdir, "Test", "base64boiData.txt"), "r") as f:
            data = f.read()

        downloadImages([data], "testing", path.join(curdir, "Images"))

        #assert path.isdir(downloadDir)
        assert imageEqualsImage("base64boi.png", downloadDir, "testing0.png")

        remove(path.join(downloadDir, "testing0.png"))
        rmdir(downloadDir)

        #assert not path.isdir(downloadDir)

        out, err = capfd.readouterr()
        assert out == """Successfully created the directory .\\Images\\testing
Image encoded in base64
\033[0;32mImage downloaded\033[0m
"""

    def test_chopped_url(self, capfd):
        downloadDir = path.join(curdir, "Images", "testing")

        downloadImages(["https://vignette.wikia.nocookie.net/mspaintadventures/images/5/5b/Trolls_looking_at_green_sun.png/revision/latest/scale-to-width-down/340?cb=20180118110537",
            "https://vignette.wikia.nocookie.net/mspaintadventures/images/5/5b/Trolls_looking_at_green_sun.png"],
            "testing", path.join(curdir, "Images"))

        with open(path.join(curdir, "Test", "base64boiData.txt"), "r") as f:
            data = f.read()

        assert imageEqualsImage("trolls.png", downloadDir, "testing0.png")
        assert imageEqualsImage("trolls.png", downloadDir, "testing1.png")

        remove(path.join(downloadDir, "testing0.png"))
        remove(path.join(downloadDir, "testing1.png"))
        rmdir(downloadDir)

        out, err = capfd.readouterr()
        assert out == """Successfully created the directory .\\Images\\testing

Getting image from: https://vignette.wikia.nocookie.net/mspaintadventures/images/5/5b/Trolls_looking_at_green_sun.png/revision/latest/scale-to-width-down/340?cb=20180118110537
Chopped image URL: https://vignette.wikia.nocookie.net/mspaintadventures/images/5/5b/Trolls_looking_at_green_sun.png
\033[0;32mImage downloaded\033[0m

Getting image from: https://vignette.wikia.nocookie.net/mspaintadventures/images/5/5b/Trolls_looking_at_green_sun.png
\033[0;32mImage downloaded\033[0m
"""

    def test_invalid_image_url(self, capfd):
        downloadDir = path.join(curdir, "Images", "testing")

        downloadImages(["notaURL"], "testing", path.join(curdir, "Images"))

        rmdir(downloadDir)

        out, err = capfd.readouterr()
        assert out == """Successfully created the directory .\\Images\\testing

Getting image from: notaURL
\033[0;31mSomething went wrong when downloading image\033[0m
"""


class TestMoveToServer:
    
    def test_missing_input_parameter(self):
        with pytest.raises(ValueError):
            moveToServer("donkeys", '', 'moore.mcmaster.ca', '', '')

    

