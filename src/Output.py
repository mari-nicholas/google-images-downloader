## @file Output.py
#  @author Samuel Crawford, Joshua Guinness
#  @brief Provides the functionality for downloading images.
#  @date 03/19/2020

from base64 import b64decode
from math import ceil, log
from os import extsep, mkdir, path, chdir
<<<<<<< HEAD
import sys
from socket import timeout as SocketTimeout
import socket
=======
>>>>>>> bc66267462a46848410e4abc01f43c83e920c91a
from sys import stdout

from imghdr import what
from urllib.error import URLError
from urllib.request import Request, urlopen

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException, BadHostKeyException
from paramiko import ssh_exception
from paramiko.buffered_pipe import PipeTimeout as PipeTimeout
from scp import SCPClient, SCPException
<<<<<<< HEAD
import shutil
from shutil import rmtree

=======
from shutil import rmtree
from socket import gaierror
from socket import timeout as SocketTimeout
>>>>>>> bc66267462a46848410e4abc01f43c83e920c91a

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

                if not img.endswith(ext):
                    start = img.rfind(ext)
                    if start > 0:
                        # strips anything after the file extension
                        img = img[:start + len(ext)]
                        print("Chopped image URL:", img)
                        data = getRequest(img)
                    else:
                        colourMsg("Unrecognized file format", 31)
                        continue

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
        raise ValueError("No input specified for hostname, username, and/or password")

    colourMsg("\nTransferring image files to the specified server...\n",
              "38;2;255;0;140")

    # Gets the current local location of the images
    dr = path.join(direc, key)

    # Function to show progress bars in console
    def progress(filename, size, sent):
        p = float(sent) / float(size) * 100
        sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, p))

    ssh = createSSH(shost, suser, spass)

    try:

        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport(), progress=progress)
        # Puts the images onto he server and closes the connection
        scp.put(dr, recursive=True)

    except SCPException as e:
        print("Operation error: %s" % e)
    except SocketTimeout:
        """
        the fetcher will need multiple attempts if the ssh connection is bad and/or the copy dir is big
        """
        print('SocketTimeout')
    except PipeTimeout as pipetimeout:
        print("timeout was reached on a read from a buffered Pipe: %s" % pipetimeout)
    finally:
        scp.close()


    # Delete the local copy of the images
    chdir(dr)
    chdir('../')
    rmtree(key)

    colourMsg("\nTransfer complete!", "38;2;255;0;140")

def createSSH(shost, suser, spass):
    try:

        # Creates and configures ssh client
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(shost, username=suser, password=spass, timeout=4000)

    except AuthenticationException:
        print("Authentication failed, please verify your credentials")
        # raise AuthenticationException
    except SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)
    except BadHostKeyException as badHostKeyException:
        print("Unable to verify server's host key: %s" % badHostKeyException)
    except socket.gaierror:
        print("Unable to find server with specified hostname")
    except ssh_exception.NoValidConnectionsError:
        print("There was an error creating a connection to the server")

    return ssh

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
            print("Creation of the directory %s failed" % d)
        else:
            print("Successfully created the directory %s" % d)
    else:
        print("Directory %s already exists" % d)


## @brief prints string wrapped in colour markers
#  @param s the string to be wrapped
#  @param n the colour tag
def colourMsg(s, n):
    print("\033[0;" + str(n) + "m" + s + "\033[0m")
