## @file Output.py
#  @author Samuel Crawford, Joshua Guinness
#  @brief Provides the functionality for downloading images.
#  @date 03/16/2020

from imghdr import what
from os import curdir, extsep, mkdir, path
from urllib.error import URLError
from urllib.request import Request, urlopen


## @brief downloads images
#  @details creates the given directory if it doesn't exist;
#  iterates through a list of image URLs and retrives them;
#  processes file extensions and saves the images to the directory
#  @param lst a list of image URLs as strings
#  @param key the keyword being searched for
#  @param loc the directory to save the images to
def downloadImages(lst, key, loc=path.join(curdir, "Images")):
    dr = path.join(loc, key)
    createDir(loc, dr)
    fileNum = 0

    for img in lst:
        print("Getting image from:", img)

        try:
            data = getRequest(img)
            ext = what("", data) # reads file extension
            if not img.endswith(ext):
                img = img[:img.rfind(ext)+len(ext)] # strips anything after the file extension
                print("Chopped image URL: ", img)
                data = getRequest(img)
        except URLError:
            print("Couldn't find image URL")
        except Exception as e:
            print("Something went wrong when downloading image")

        with open(path.join(dr, key + str(fileNum) + extsep + ext), 'wb') as f:
            f.write(data)
        print('\033[0;32m' + "Image downloaded\n" + '\033[0m')

        fileNum += 1

## @brief retrieves image data for the image
#  @details uses the urllib library to create a request object
#  to read the image data
#  @param img the image URL
def getRequest(img):
    req = Request(img, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
    response = urlopen(req)
    data = response.read()
    response.close()

    return data

## @brief creates the given directory d in loc if non-existent
#  @param loc the parent directory
#  @param d   the name of the subdirectory for images
def createDir(loc, d):
    if path.isdir(loc) and not path.exists(d):        
        try:
            mkdir(d)
        except Exception as e:
            print ("Creation of the directory %s failed" % d)
        else:
            print ("Successfully created the directory %s " % d)
    else:
        print("Directory %s already exists" % d)
