# Secrets: The format and structure of the output data.
# Services: Converts the processed data into output files/folders that will be written to storage

from imghdr import what
from os import curdir, mkdir, path
from urllib.request import Request, urlopen

def downloadImages(lst, key, loc=path.join(curdir, "Images")):
    d = createDir(loc, key)
    fileNum = 0

    for img in lst:
        print("Getting image from:", img)

        try:
            data = getRequest(img)
            ext = what("", data) # reads file extension
            if not img.endswith(ext):
                img = img[:img.rfind(ext)+len(ext)] # strips anything after the file extension
                data = getRequest(img)
        except Exception as e:
            # print(e)
            print("Something went wrong when downloading image")

        try:
            output_file = open(path.join(d, key + str(fileNum) + "." + what("", data)), 'wb')
            output_file.write(data)
            output_file.close()
            print('\033[0;32m' + "Image downloaded\n" + '\033[0m')
        except Exception as e:
            # print(e)
            print("Something went wrong when saving image")

        fileNum += 1

def getRequest(img):
    req = Request(img, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
    response = urlopen(req)
    data = response.read()
    response.close()

    return data

def createDir(loc, key):
    d = path.join(loc, key)

    if path.isdir(loc) and not path.exists(d):        
        try:
            mkdir(d)
        except Exception as e:
            # print(e)
            print ("Creation of the directory %s failed" % d)
        else:
            print ("Successfully created the directory %s " % d)
    else:
        print("Directory %s already exists" % d)

    return d

# downloadImages(["https://vignette.wikia.nocookie.net/mspaintadventures/images/5/5b/Trolls_looking_at_green_sun.png/revision/latest/scale-to-width-down/340?cb=20180118110537", 
#     "https://www.homestuck2.com/assets/panels/0075.gif"], "homestuck")
