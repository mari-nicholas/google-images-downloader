## @file Input.py
#  @author Nicholas Mari, Samuel Crawford
#  @brief Generates a dictionary of parameters that will be used to search for images
#  @date 03/31/2020

# Secrets: The format and structure of the input data.
# Services: Converts  the  input  data  into  the  data  structure  used  by  the  input  parameters module.

from argparse import ArgumentParser
from json import load
from os import curdir, path
from platform import system


## @brief builds dictionary of input arguments
#  @details Takes input from the user as arguments and builds a dictionary with
#  the input that will be used to build a search url
#  @return args dictionary of all the command line arguments with their respective values from the user input
def userInput():
    parser = ArgumentParser()
    parser.add_argument('-ff', '--fromfile', default='', help='gets args from file; takes file path to .txt file')

    # Want this function so it doesn't give error when parsing with unknown args
    fileArg = parser.parse_known_args()

    # Turns it into a dict
    fileArg = vars(fileArg[0])

    if(fileArg['fromfile']):
        return keywordFromFile(fileArg['fromfile'])
    else:
        cmdParser = ArgumentParser()
        cmdParser.add_argument('-k', '--keyword', required=True, help='keyword for the Google images you want')
        cmdParser.add_argument('-l', '--limit', type=int, default=10, help='limit for the number of images you want')
        cmdParser.add_argument('-ss', '--safesearch', default=False, help='turns on safe search', action='store_true')
        cmdParser.add_argument('-ft', '--filetype', default='', help='download images of specific file type',
                               choices=['jpg', 'gif', 'png', 'bmp', 'svg', 'webp', 'ico', 'raw'])
        cmdParser.add_argument('-d', '--directory', default=path.join(curdir, 'Images'), help='download images to folder in a specific directory')
        cmdParser.add_argument('-c', '--colour', default='', help='search for images with specific colours',
                               choices=['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown', 'full-color', 'black-and-white', 'transparent'])
        cmdParser.add_argument('-li', '--license', default='', help='search based on what image is licensed for',
                               choices=['labeled-for-reuse-with-modifications', 'labeled-for-reuse', 'labeled-for-noncommercial-reuse-with-modification', 'labeled-for-nocommercial-reuse'])
        cmdParser.add_argument('-t', '--imagetype', default='', help='search for a specific type of image',
                               choices=['face', 'photo', 'clipart', 'line-drawing', 'animated'])
        cmdParser.add_argument('-a', '--imageage', default='', help='search for how long ago the image was uploaded',
                               choices=['past-24-hours', 'past-7-days', 'past-month', 'past-year'])
        cmdParser.add_argument('-ar', '--aspectratio', default='', help='search based on the aspect ratio of the image',
                               choices=['tall', 'square', 'wide', 'panoramic'])
        cmdParser.add_argument('-is', '--imagesize', default='', help='search based on approximate size of image desired',
                               choices=['large', 'medium', 'icon', '>400*300', '>640*480', '>800*600', '>1024*768', '>2MP', '>4MP', '>6MP', '>8MP', '>10MP', '>12MP', '>15MP', '>20MP', '>40MP', '>70MP'])
        cmdParser.add_argument('-s', '--serverhost', default='', help='specify a server hostname to download the images to')
        cmdParser.add_argument('-u', '--serverusername', default='', help='specify a server username')
        cmdParser.add_argument('-p', '--serverpassword', default='', help='specify a server password')
        # cmdParser.add_argument('-rp', '--remotepath', default='', help='specify a remote path to save the images to')
        cmdParser.add_argument('-wl', '--whitelist', default='', help='only get images from a specified website or domain')
        cmdParser.add_argument('-rg', '--region', default='', help='get images uploaded in a specific region',
                               choices=['Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antigua & Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia & Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'Colombia', 'Congo - Brazzaville', 'Congo - Kinshasa', 'Cook Islands', 'Costa Rica', 'Cote d\'Ivoire', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Guatemala', 'Guernsey', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Samoa', 'San Marino', 'Sao Tome & Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'St. Helena', 'St. Vincent & Grenadines', 'Suriname', 'Sweden', 'Switzerland', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'U.S. Virgin Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Zambia', 'Zimbabwe'])
        cmdParser.add_argument('-bl', '--blacklist', default='', help='Stop program from downloading images from specified websites')

        args = vars(cmdParser.parse_args())
        return args


## @brief builds dictionary of input arguments from a file
#  @details uses a filepath provided by the user to build a dictionary of
#  the arguments that will be used to build a search url
#  @return args dictionary of all the command line arguments with their respective values from the user input
def keywordFromFile(filePath):
    try:
        f = open(filePath)
    except Exception:
        msg = "Could not find the file you specified."
        if system() == "Windows":
            msg += " If you are on Windows, make sure your file path uses " + \
                "double backslashes (\\\\) rather than single backslashes (\\)"
        raise Exception(msg)

    args = load(f)

    if "keyword" not in args:
        raise ValueError("keyword not found")

    for key in ["filetype", "colour", "license", "imagetype", "imageage",
                "imagesize", "aspectratio", "serverhost", "serverusername",
                "serverpassword", "whitelist", "region", "blacklist"]:
        if key not in args:
            args[key] = ""

    if "limit" not in args:
        args["limit"] = 10
    if "safesearch" not in args:
        args["safesearch"] = False
    if "directory" not in args:
        args["directory"] = path.join(curdir, 'Images')

    f.close()
    return args
