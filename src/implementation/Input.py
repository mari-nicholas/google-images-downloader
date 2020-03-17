# Secrets: The format and structure of the input data.
# Services: Converts  the  input  data  into  the  data  structure  used  by  the  input  parameters module.

import argparse

def UserInput():
	fileCheck = argparse.ArgumentParser()
	fileCheck.add_argument('-f', '--file', default='', type=str, required=False, help='gets args from file. Takes file path to .txt file')

	fileArg = fileCheck.parse_args()

	if(fileArg.file):
		return keywordFromFile(fileArg.file)
	else:
		parser = argparse.ArgumentParser()
		parser.add_argument('-k', '--keyword', required=True , help='Keyword for the google images you want')
		parser.add_argument('-l', '--limit', help='Limit for the number of images you want')

		args = fileCheck.parse_args()
		print('User Input Function')


def keywordFromFile(filePath):
    print('Keyword From File Function')


if __name__ == '__main__':
	UserInput()