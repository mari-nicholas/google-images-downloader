## @file Output.py
#  @author Samuel Crawford, Joshua Guinness
#  @brief Provides the functionality for downloading images.
#  @date 03/31/2020

from base64 import b64decode
from math import ceil, log
from os import extsep, mkdir, path, chdir
from shutil import rmtree
from sys import stdout

from imghdr import what
from urllib.request import Request, urlopen

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient


## @brief downloads images
#  @details creates the given directory if it doesn't exist;
#  iterates through a list of image URLs and retrives them;
#  processes file extensions and saves the images to the directory
#  @param lst a list of image URLs as strings
#  @param key the keyword being searched for
#  @param loc the directory to save the images to
def downloadImages(lst, key, loc):
    dr = path.join(loc, key)
    createDir(dr)
    fileNum, places = 0, ceil(log(len(lst), 10))

    for img in lst:

        try:
            # allows for downloading base64 images
            if img.startswith("data:image"):
                base = img.find(";base64,")
                ext = img[11:base]
                img = img[base + 8:]
                print("Image encoded in base64")
                data = b64decode(img)
            else:
                print("\nGetting image from:", img)
                data = getRequest(img)
                ext = what("", data)  # reads file extension
                if ext == "jpeg" and ext not in img:  # circumvents jpg bug
                    ext = "jpg"
                elif not ext:
                    if ".jpg" in img:
                        ext = "jpg"
                    else:
                        colourMsg("Unrecognized file format", 31)
                        continue

                if ext in img and not img.endswith(ext):
                    if ext == "jpeg" and ".jpg" in img:
                        start = img.rfind("jpg")
                    else:
                        start = img.rfind(ext)

                    if start > 0:
                        # strips anything after the file extension
                        img = img[:start + len(ext)]
                        print("Chopped image URL:", img)
                        data = getRequest(img)

        except Exception:
            colourMsg("Something went wrong when downloading image", 31)
            continue

        # Might be needed in future to avoid "mismatch between tag" WinError
        # if ext == "jpg":
        #     ext = "jpeg"

        filename = key + str(fileNum).zfill(places) + extsep + ext
        with open(path.join(dr, filename), 'wb') as f:
            f.write(data)

        colourMsg("Image downloaded", 32)

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

    if (shost == '' or suser == '' or spass == ''):
        e = "No input specified for hostname, username, and/or password"
        raise ValueError(e)

    colourMsg("\nTransferring image files to the specified server...\n",
              "38;2;255;0;140")

    # Gets the current local location of the images
    dr = path.join(direc, key)

    # Function to show progress bars in console
    def progress(filename, size, sent):
        p = float(sent) / float(size) * 100
        stdout.write("%s\'s progress: %.2f%%   \r" % (filename, p))

    ssh = createSSH(key, direc, shost, suser, spass)

    try:

        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport(), progress=progress)
        # Puts the images onto he server and closes the connection
        scp.put(dr, recursive=True)

    except Exception as error:
        print("There was an error transferring your images to the server")
        print(error)
        scp.close()
        deleteLocalImageFolder(direc, key)
        raise

    scp.close()

    # Delete the local copy of the images
    deleteLocalImageFolder(direc, key)

    colourMsg("\nTransfer complete!", "38;2;255;0;140")


## @brief creates and configures ssh client
#  @param key the keyword being searched for
#  @param direc local directory where the images are
#  @param shost hostname of the server
#  @param suser the username to access the server
#  @param spass the password associated with the username
#  to access the server
#  @return ssh client
def createSSH(key, direc, shost, suser, spass):

    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(shost, username=suser, password=spass, timeout=4000)

    except Exception as error:
        print("There was an issue with creating an SSH Object")
        print("Please that all your parameters are correct \
            and the server exists and is running.\n")
        print(error)
        deleteLocalImageFolder(direc, key)
        raise

    return ssh


## @brief deletes the local image folder once it
#  is moved to the server
#  @param direc local directory where the images are
#  @param key the keyword being searched for
def deleteLocalImageFolder(direc, key):
    chdir(direc)
    rmtree(key)


## @brief retrieves image data for the image
#  @details uses the urllib library to create a request object
#  to read the image data
#  @param img the image URL
def getRequest(img):
    h = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 " + \
        "(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = Request(img, headers={"User-Agent": h})
    response = urlopen(req)
    data = response.read()
    response.close()

    return data


## @brief creates the given directory d if non-existent
#  @param d the name of the directory to create
def createDir(d):
    if not path.exists(d):
        try:
            mkdir(d)
        except Exception:
            raise OSError("Creation of the directory %s failed" % d)
        else:
            print("Successfully created the directory %s" % d)
    else:
        print("Directory %s already exists" % d)


## @brief prints string wrapped in colour markers
#  @param s the string to be wrapped
#  @param n the colour tag
def colourMsg(s, n):
    print("\033[0;" + str(n) + "m" + s + "\033[0m")
