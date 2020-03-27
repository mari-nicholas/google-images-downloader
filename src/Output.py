## @file Output.py
#  @author Samuel Crawford, Joshua Guinness
#  @brief Provides the functionality for downloading images.
#  @date 03/19/2020

from base64 import b64decode
from math import ceil, log
from os import curdir, extsep, mkdir, path, getcwd, chdir
import sys

from imghdr import what
from urllib.error import URLError
from urllib.request import Request, urlopen

from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient
import shutil


## @brief downloads images
#  @details creates the given directory if it doesn't exist;
#  iterates through a list of image URLs and retrives them;
#  processes file extensions and saves the images to the directory
#  @param lst a list of image URLs as strings
#  @param key the keyword being searched for
#  @param loc the directory to save the images to
def downloadImages(lst, key, loc):
    dr = path.join(loc, key)
    createDir(loc, dr)
    fileNum, places = 0, ceil(log(len(lst), 10))

    for img in lst:
        print("\nGetting image from:", img)

        try:
            data = getRequest(img)
            if img.startswith("data:image"): # allows for downloading base64 images
                base = img.find(";base64,")
                ext = img[11:base]
                img = img[base+8:]
                print("Encoded in base64: ", img)
                data = b64decode(img)
            else:
                ext = what("", data) # reads file extension
                if ext == "jpeg" and ext not in img: # circumvents jpg bug
                    ext = "jpg"
                    data = getRequest(img)
                elif not ext:
                    if "jpg" in img:
                        ext = "jpg"
                    else:
                        print("\033[0;31mUnrecognized file format\033[0m")
                        continue

                if not img.endswith(ext):
                    start = img.rfind(ext)
                    if start > 0:
                        img = img[:start+len(ext)] # strips anything after the file extension
                        print("Chopped image URL: ", img)
                        data = getRequest(img)
                    else:
                        print("\033[0;31mUnrecognized file format\033[0m")
                        continue

        except URLError:
            print("\033[0;31mCouldn't find image URL\033[0m")
            continue
        except Exception as e:
            print("\033[0;31mSomething went wrong when downloading image\033[0m")
            continue

        # Might be needed in future to avoid "mismatch between tag" WinError
        # if ext == "jpg":
        #     ext = "jpeg"

        with open(path.join(dr, key + str(fileNum).zfill(places) + extsep + ext), 'wb') as f:
            f.write(data)
        print('\033[0;32m' + "Image downloaded" + '\033[0m')

        fileNum += 1


## @brief moves all images to a specified server
#  @details after downloading the images locally,
#  scp's all the images to a specified server, then
#  deletes the local copy of the images
#  @param key the keyword being searched for
#  @param direc local directory where the images are
#  @param shost hostname of the server
#  @param suser the username to access the server
#  @param spass the password associated with the username
#  to access the server
def moveToServer(key, direc, shost, suser, spass):
    
    print('\033[38;2;255;0;140m' + 
          "\nTransfering image files to the specified server...\n" + 
          '\033[0m')

    try: 

        # Gets the current local location of the images
        dr = path.join(direc, key)

        # Creates and configures ssh client
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(shost, username=suser, password=spass, timeout=5000)

        # Function to show progress bars in console
        def progress(filename, size, sent):
            sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport(), progress=progress)

        # Puts the images ont he server and closes the connection
        scp.put(dr, recursive=True)
        scp.close()

        # Delete the local copy of the images
        chdir(dr)
        chdir('../')
        shutil.rmtree(key)

    except:
        print("There was an issue copying them to the server")

    print('\033[38;2;255;0;140m' + 
          "\nTransfer complete!" + 
          '\033[0m')

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
    newDir = path.join(loc, d)
    if not path.exists(newDir):
        try:
            mkdir(newDir)
        except Exception as e:
            print("Creation of the directory %s failed" % d)
        else:
            print("Successfully created the directory %s" % d)
    else:
        print("Directory %s already exists" % d)
