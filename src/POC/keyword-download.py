import argparse
import sys
import urllib.request
from urllib.parse import quote
from urllib.request import Request, urlopen

def user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="keyword for the google images you want")
    parser.add_argument("limit", help="limit for the number of images you want")
    args = parser.parse_args()
    return args.keyword, args.limit

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
        return data
    except Exception as e:
        print("Could not get page URL")
        sys.exit()

def get_image_url(raw_html):
    start = raw_html.find('class="rg_i Q4LuWd tx8vtf"')
    if start == -1:  # If no links are found then give an error!
        end = 0
        link = "no_links"
        return link, end   
    else:
        # type_of_image = get_image_type(start, raw_html)
        #These lines isolate the link in the raw_html
        beg_link = raw_html.find('data-iurl="', start+1)
        end_link = raw_html.find('jsname="', beg_link+1)
        link = str(raw_html[beg_link+11:end_link-2])
        return link, end_link

# def get_image_type(start, raw_html):
#     try:
#         beg_type = raw_html.find('src="data:image/', start)
#         end_type = raw_html.find(';', beg_type+1)
#         type_of_image = str(raw_html[beg_type+16:end_type])
#         return type_of_image
#     except Exception as e:
#         print("Could not find image type")
#         sys.exit()

def write_to_file(image_url, keyword, i):
     try:
         req = Request(image_url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
         response = urlopen(req)
         data = response.read()
         response.close()
         path = "Images/" + keyword + str(i) + ".jpeg" 
         output_file = open(path, 'wb')
         output_file.write(data)
         output_file.close()
     except Exception as e:
         print("Something went wrong when downloading and saving image")


def download_images(raw_html, keyword, limit):
    sliced_html = raw_html
    for i in range(0, limit):
        #Gets Links
        image_url, cutoff = get_image_url(sliced_html)
        #No links => End Program 
        if(image_url == "no_links"):
            break
        else:
            print("Getting thumbnail from:\t", image_url)
            write_to_file(image_url, keyword, i)
            print('\033[0;32m' + "Image", (i+1), "downloaded\n" + '\033[0m')
            sliced_html = sliced_html[cutoff:]


def main():
    keyword, limit = user_input()

    url = construct_url(keyword)
    raw_html = get_html(url)

    print('\033[1;33m' + "\nDownloading Images...\n" + '\033[0m')
    download_images(raw_html, keyword, int(limit))
    print('\033[1;32m' + "Download Complete\n" + '\033[0m')

if __name__ == '__main__':
    main()
    