import argparse
import sys
import urllib.request
from urllib.parse import quote
from urllib.request import Request, urlopen

def user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="keywords of google images you want")
    args = parser.parse_args()
    return args.keyword

def construct_url(keyword):

    params = '&tbm='

    url = 'https://www.google.com/search?q=' + quote(
                keyword.encode('utf-8')) + '&espv=2&sxsrf=ACYBGNSwqBUElVjmEWOTu3-mXPnReqFoLw:1581376760401&source=lnms' + params + 'isch&sa=X&ved=2ahUKEwiY7bzAj8jnAhUQjq0KHbXwBEYQ_AUoAXoECBMQAw&biw=838&bih=880'

    return url
   
def get_html(url):
    #Requests HTML using urllib library
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = str(response.read())
        #print("URL Read\n")
        return data
    except Exception as e:
        print("Could not open URL.")
        sys.exit()

def get_image_url(raw_html):
    start = raw_html.find('class="rg_i Q4LuWd tx8vtf"')
    if start == -1:  # If no links are found then give an error!
        end = 0
        link = "no_links"
        return link, end   
    else:
        #These lines isolate the link in the raw_html
        beg_link = raw_html.find('data-iurl="', start+1)
        end_link = raw_html.find('jsname="', beg_link+1)
        link = str(raw_html[beg_link+11:end_link-2])
        return link, end_link

def download_images(raw_html):
    limit = 1
    i = 0
    for i in range(0, limit):
        #Gets Links
        image_url, cutoff = get_image_url(raw_html)  
        #No links => End Program 
        if(image_url == "no_links"):
            break
        else:
#           print(image_url)
            print("Image", (i+1), "Downloaded...\n")

def main():
    keyword = user_input()

    url = construct_url(keyword)
    raw_html = get_html(url)

    print("Downloading Images...")
    download_images(raw_html)
    print("Download Complete")

if __name__ == '__main__':
    main()