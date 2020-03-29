#  @file NavigatePage.py
#  @author Nicholas Mari
#  @brief Generates a dictionary of parameters that will be used to search for images
#  @date 03/24/2020

# Secrets: The format and structure of the input data.
# Services: Converts  the  input  data  into  the  data  structure  used  by  the  input  parameters module.

from argparse import ArgumentParser
from json import load
from os import curdir, path

#  @brief builds dictionary of input arguments
#  @details Takes input from the user as arguments and builds a dictionary with
#  the input that will be used to build a search url
#  @return args dictionary of all the command line arguments with their respective values from the user input
def userInput():
	parser = ArgumentParser()
	parser.add_argument('-ff', '--fromfile', default='', type=str, required=False, help='gets args from file. Takes file path to .txt file')

	#Want this function so it doesn't give error when parsing with unknown args
	fileArg = parser.parse_known_args()

	#Turns it into a dict
	fileArg = vars(fileArg[0])

	if(fileArg['fromfile']):
		return keywordFromFile(fileArg['fromfile'])
	else:
		cmdParser = ArgumentParser()
		cmdParser.add_argument('-k', '--keyword', required=True, help='Keyword for the google images you want')
		cmdParser.add_argument('-l', '--limit', type=int, default=10, help='Limit for the number of images you want')
		cmdParser.add_argument('-ss', '--safesearch', default=False, help="Turns on safe search", action='store_true')
		cmdParser.add_argument('-ft', '--filetype', type=str, required=False, default='', help='download images of specific file type', choices=['jpg', 'gif', 'png', 'bmp', 'svg', 'webp', 'ico', 'raw'])
		cmdParser.add_argument('-d', '--directory', type=str, required=False, default=path.join(curdir, "Images"), help='download images to folder in a specific directory')
		cmdParser.add_argument('-c', '--colour', type=str, required=False, default='', help='search for images with specific colours', choices=['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown', 'full-color', 'black-and-white', 'transparent'])
		cmdParser.add_argument('-li', '--license', type=str, required=False, default='', help='search based on what image is licensed for', choices=['labeled-for-reuse-with-modifications','labeled-for-reuse','labeled-for-noncommercial-reuse-with-modification','labeled-for-nocommercial-reuse'])
		cmdParser.add_argument('-t', '--imagetype',  type=str, required=False, default='',  help='search for a specific type of image', choices=['face','photo','clipart','line-drawing','animated'])
		cmdParser.add_argument('-a', '--imageage', type=str, required=False, default='', help='search for how long ago the image was uploaded', choices=['past-24-hours','past-7-days','past-month','past-year'])
		cmdParser.add_argument('-ar', '--aspectratio', type=str, required=False, default='', help='search based on the aspect ratio of the image', choices=['tall', 'square', 'wide', 'panoramic'])
		cmdParser.add_argument('-is', '--imagesize', type=str, required=False, help='search based on approximate size of image desired', choices=['large','medium','icon','>400*300','>640*480','>800*600','>1024*768','>2MP','>4MP','>6MP','>8MP','>10MP','>12MP','>15MP','>20MP','>40MP','>70MP'])
		cmdParser.add_argument('-s', '--serverhost', type=str, required=False, default='', help='specify a server hostname to download the images to')
		cmdParser.add_argument('-u', '--serverusername', type=str, required=False, default='', help='specify a server username')
		cmdParser.add_argument('-p', '--serverpassword', type=str, required=False, default='', help='specify a server password')
		# cmdParser.add_argument('-rp', '--remotepath', type=str, required=False, default='', help='specify a remote path to save the images to')
		
		args = cmdParser.parse_args()


		# print(vars(args))
		#vars() Turns it into a dict
		args = vars(args)
		return args

#  @brief builds dictionary of input arguments from a file
#  @details uses a filepath provided by the user to build a dictionary of
#  the arguments that will be used to build a search url
#  @return args dictionary of all the command line arguments with their respective values from the user input
def keywordFromFile(filePath):
	#print('Keyword From File Function')
	args = {}
	f = open(filePath)
	args = json.load(f)

	return args
