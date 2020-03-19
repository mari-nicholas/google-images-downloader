# Secrets: The format and structure of the Google search query.
# Services: Converts the processed data from the input module into a URL string representingthe desired Google search query.

from urllib.parse import quote

def buildURLParam(args):
    #print("Build URL Parameters Function")

    params = ''

    #print(args)
    for i in args:
    	if args[i] and (not (i == 'keyword')) and (not (i == 'limit')) and (not (i == 'safesearch')) and (not (i == 'directory')):
    		if params:
    			params = params + ',' + args[i]
    		else:
    			params += args[i]

    params = '&tbm=' + params

    return params

def buildURL(args):
    #print("Build URL Function")

    params = buildURLParam(args)

    url = 'https://www.google.com/search?q=' + quote(args['keyword'].encode('utf-8')) + '&espv=2&sxsrf=ACYBGNSwqBUElVjmEWOTu3-mXPnReqFoLw:1581376760401&source=lnms' + params + 'isch&sa=X&ved=2ahUKEwiY7bzAj8jnAhUQjq0KHbXwBEYQ_AUoAXoECBMQAw&biw=838&bih=880'

    if(args['safesearch']):
    	url += "&safe=active"

    print(url)

if __name__ == '__main__':
	buildURL({'keyword': 'test', 'limit': 100, 'safesearch': False, 'filetype': '', 'directory': '', 'colour': '', 'colourtype': '', 'liscence': '', 'imagetype': '', 'imageage': '', 'aspectratio': ''})