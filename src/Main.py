## @file Main.py
#  @author Samuel Crawford
#  @brief Provides the control of the entire program
#  @date 03/31/2020

from Input import userInput
from NavigatePage import getImageURL
from SearchQuery import buildURL
from Output import downloadImages, moveToServer


## @brief Controls the flow of data in the program
#  @details Calls all other functions, storing their output as variables
#  to be passed to other functions
def main():
    args = userInput()
    url = buildURL(args)
    urls = getImageURL(url, args["limit"], args['blacklist'])
    downloadImages(urls, args["keyword"], args["directory"])
    if (args["serverhost"] != ""):
        moveToServer(args["keyword"], args["directory"], args["serverhost"],
                     args["serverusername"], args["serverpassword"])


if __name__ == '__main__':
    main()
