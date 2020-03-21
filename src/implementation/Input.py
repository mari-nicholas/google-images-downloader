# Secrets: The format and structure of the input data.
# Services: Converts  the  input  data  into  the  data  structure  used  by  the  input  parameters module.

from argparse import ArgumentParser
from json import load
from os import curdir, path

def userInput():
	parser = ArgumentParser()
	parser.add_argument('-f', '--file', default='', type=str, required=False, help='gets args from file. Takes file path to .txt file')

	#Want this function so it doesn't give error when parsing with unknown args
	fileArg = parser.parse_known_args()

	#Turns it into a dict
	fileArg = vars(fileArg[0])

	if(fileArg['file']):
		return keywordFromFile(fileArg['file'])
	else:
		cmdParser = ArgumentParser()
		cmdParser.add_argument('-k', '--keyword', required=True, help='Keyword for the google images you want')
		cmdParser.add_argument('-l', '--limit', type=int, default=100, help='Limit for the number of images you want')
		cmdParser.add_argument('-ss', '--safesearch', default=False, help="Turns on safe search", action='store_true')
		cmdParser.add_argument('-ft', '--filetype', type=str, required=False, default='', help='download images of specific file type', choices=['jpg', 'gif', 'png', 'bmp', 'svg', 'webp', 'ico'])
		cmdParser.add_argument('-d', '--directory', type=str, required=False, default=path.join(curdir, "Images"), help='download images to folder in a specific directory')
		cmdParser.add_argument('-c', '--colour', type=str, required=False, default='', help='search for images with specific colours', choices=['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown'])
		cmdParser.add_argument('-ct', '--colourtype', type=str, required=False, default='', help='seach for specific colour type of image', choices=['full-color', 'black-and-white', 'transparent'])
		cmdParser.add_argument('-li', '--license', type=str, required=False, default='', help='search based on what image is licensed for', choices=['labeled-for-reuse-with-modifications','labeled-for-reuse','labeled-for-noncommercial-reuse-with-modification','labeled-for-nocommercial-reuse'])
		cmdParser.add_argument('-t', '--imagetype',  type=str, required=False, default='',  help='search for a specific type of image', choices=['face','photo','clipart','line-drawing','animated'])
		cmdParser.add_argument('-a', '--imageage', type=str, required=False, default='', help='search for how long ago the image was uploaded', choices=['past-24-hours','past-7-days','past-month','past-year'])
		cmdParser.add_argument('-ar', '--aspectratio', type=str, required=False, default='', help='search based on the aspect ratio of the image', choices=['tall', 'square', 'wide', 'panoramic'])
		cmdParser.add_argument('-s', '--serverhost', type=str, required=False, default='', help='specify a server hostname to download the images to')
		cmdParser.add_argument('-u', '--serverusername', type=str, required=False, default='', help='specify a server username')
		cmdParser.add_argument('-p', '--serverpassword', type=str, required=False, default='', help='specify a server password')
		cmdParser.add_argument('-rp', '--remotepath', type=str, required=False, default='', help='specify a remote path to save the images to')
		
		args = cmdParser.parse_args()


		# print(vars(args))
		#vars() Turns it into a dict
		return vars(args)

def keywordFromFile(filePath):
	#print('Keyword From File Function')
	args = {}
	f = open(filePath)
	args = json.load(f)

	return args
