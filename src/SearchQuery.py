# Secrets: The format and structure of the Google search query.
# Services: Converts the processed data from the input module into a URL string representingthe desired Google search query.

from urllib.parse import quote

def buildURLParam(args):
    searchArgs = {	'aspectratio' : args['aspectratio'],
    				'colour' : args['colour'],
    				'colourtype' : args['colourtype'],
    				'filetype' : args['filetype'],
    				'imageage' : args['imageage'],
    				'imagesize' : args['imagesize'],
    				'imagetype' : args['imagetype'],
    				'license' : args['license']
    			 }

   	#This contains all the equivalent text that will be used in the url rather than what is input at the command line
   	#For example, in the url Red will become ic:specific,isc:red
    urlFormats = {	'red' : 'ic:specific,isc:red',
    				'orange' : 'ic:specific,isc:orange',
    				'yellow':'ic:specific,isc:yellow',
    				'green':'ic:specific,isc:green',
    				'teal':'ic:specific,isc:teal',
    				'blue':'ic:specific,isc:blue',
    				'purple':'ic:specific,isc:purple', 
    				'pink':'ic:specific,isc:pink', 
    				'white':'ic:specific,isc:white', 
    				'gray':'ic:specific,isc:gray', 
    				'black':'ic:specific,isc:black',
    				'brown':'ic:specific,isc:brown',
    				'full-color':'ic:color',
    				'black-and-white':'ic:gray',
    				'transparent':'ic:trans',
    				'labeled-for-reuse-with-modifications':'sur:fmc',
    				'labeled-for-reuse':'sur:fc',
    				'labeled-for-noncommercial-reuse-with-modification':'sur:fm',
    				'labeled-for-nocommercial-reuse':'sur:f',
    				'large':'isz:l',
    				'medium':'isz:m',
    				'icon':'isz:i',
    				'>400*300':'isz:lt,islt:qsvga',
    				'>640*480':'isz:lt,islt:vga',
    				'>800*600':'isz:lt,islt:svga',
    				'>1024*768':'visz:lt,islt:xga',
    				'>2MP':'isz:lt,islt:2mp',
    				'>4MP':'isz:lt,islt:4mp',
    				'>6MP':'isz:lt,islt:6mp',
    				'>8MP':'isz:lt,islt:8mp',
    				'>10MP':'isz:lt,islt:10mp',
    				'>12MP':'isz:lt,islt:12mp',
    				'>15MP':'isz:lt,islt:15mp',
    				'>20MP':'isz:lt,islt:20mp',
    				'>40MP':'isz:lt,islt:40mp',
    				'>70MP':'isz:lt,islt:70mp',
    				'face':'itp:face',
    				'photo':'itp:photo',
    				'clipart':'itp:clipart',
    				'line-drawing':'itp:lineart',
    				'animated':'itp:animated',
    				'past-24-hours':'qdr:d',
    				'past-7-days':'qdr:w',
    				'past-month':'qdr:m',
    				'past-year':'qdr:y',
    				'tall':'iar:t',
    				'square':'iar:s',
    				'wide':'iar:w',
    				'panoramic':'iar:xw',
    				'jpg':'ift:jpg',
    				'gif':'ift:gif',
    				'png':'ift:png',
    				'bmp':'ift:bmp',
    				'svg':'ift:svg',
    				'webp':'webp',
    				'ico':'ift:ico'
    			 }

    params = [urlFormats[searchArgs[i]] for i in searchArgs if searchArgs[i]]

    return ",".join(params)

def buildURL(args):
    #print("Build URL Function")

    params = buildURLParam(args)

    url = 'https://www.google.com/search?q=' + quote(args['keyword'].encode('utf-8')) + \
        '&tbm=isch&hl=en&hl=en&tbs=' + quote(params.encode('utf-8')) + \
        '&ved=0CAMQ2J8EahcKEwjgteiDqrToAhUAAAAAHQAAAAAQAg&biw=1519&bih=760'

    if args['safesearch']:
    	url += "&safe=active"

    return url
