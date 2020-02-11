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

'''

#Slight Issue with this function:
#Need to extract file type from raw_HTML so we
#Can Write the File. I've left you with this
#as a jumping off point.

def write_to_file(image_url, keyword, i):
    try:
        req = Request(image_url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
        response = urlopen(req)
        data = response.read()
        response.close()
        path = "./Images/" + keyword + "/image" + str(i) 
        print(path)
        output_file = open(path, 'wb')
        output_file.write(data)
        output_file.close()
    except Exception as e:
        print("Something Went Wrong...")

'''

def download_images(raw_html, keyword):
    limit = 1
    i = 0
    sliced_html = raw_html
    for i in range(0, limit):
        #Gets Links
        image_url, cutoff = get_image_url(sliced_html)  
        #No links => End Program 
        if(image_url == "no_links"):
            break
        else:
#            print(image_url, "\n")
#            write_to_file(image_url, keyword, i)
            print("Image", (i+1), "Downloaded...\n")
            sliced_html = sliced_html[cutoff:]


def main():
    keyword = user_input()

    url = construct_url(keyword)
    raw_html = get_html(url)

    print("Downloading Images...")
    download_images(raw_html, keyword)
    print("Download Complete")

if __name__ == '__main__':
    main()