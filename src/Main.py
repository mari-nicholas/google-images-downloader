# Secrets: The control flow logic of the system.
# Services: Controls the flow of data.

from Input import userInput
from NavigatePage import getImageURL
from SearchQuery import buildURL
from Output import downloadImages, moveToServer

def main():
    args = userInput()
    url = buildURL(args)
    urls = getImageURL(url, args["limit"], args['blacklist'])
    downloadImages(urls, args["keyword"], args["directory"])
    if (args["serverhost"] != ""):
        moveToServer(args["keyword"], args["directory"], args["serverhost"], args["serverusername"], args["serverpassword"])

if __name__ == '__main__':
    main()
