# Secrets: The format and structure of the output data.
# Services: Converts the processed data into output files/folders that will be written to storage

from os import curdir, mkdir, path
from urllib.request import Request, urlopen

def downloadImages(lst, key, loc=path.join(curdir, "Images")):
    d = createDir(loc, key)

    for img in lst:
        print("Getting image from: ", img)

        try:
            req = Request(img, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req)
            data = response.read()
            response.close()
        except Exception as e:
            print(e)
            print("Something went wrong when downloading image")

        try:
            output_file = open(path.join(d, key), 'wb')
            output_file.write(data)
            output_file.close()
            print('\033[0;32m' + "Image downloaded\n" + '\033[0m')
        except Exception as e:
            print(e)
            print("Something went wrong when saving image")

def createDir(loc, key):
    if path.isdir(loc):        
        try:
            d = path.join(loc, key)
            mkdir(d)
        except Exception as e:
            print(e)
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
    else:
        print("Directory doesn't exist:", loc)

    return d

#downloadImages(["https://vignette.wikia.nocookie.net/mspaintadventures/images/5/5b/Trolls_looking_at_green_sun.png"], "homestuck")
