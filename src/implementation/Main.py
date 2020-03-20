# Secrets: The control flow logic of the system.
# Services: Controls the flow of data.

from Input import userInput
from NavigatePage import getImageURL
from SearchQuery import buildURL
from Output import downloadImages

def main():
    args = userInput()
    url = buildURL(args)
    urls = getImageURL(url, args["limit"])
    downloadImages(urls, args["keyword"], args["directory"])

if __name__ == '__main__':
    main()
