import argparse
import sys
import urllib.request
import requests
from urllib.parse import quote
from urllib.request import Request, urlopen
from lxml import html
from bs4 import BeautifulSoup

# Command line input to program
def user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="Keyword for the google images you want")
    parser.add_argument("limit", help="Limit for the number of images you want")
    args = parser.parse_args()
    return args.keyword, args.limit

# Constructs the search URL based on the keyword and established strings
def construct_url(keyword):

    params = '&tbm='
    url = 'https://www.google.com/search?q=' + quote(
                keyword.encode('utf-8')) + '&espv=2&sxsrf=ACYBGNSwqBUElVjmEWOTu3-mXPnReqFoLw:1581376760401&source=lnms' + params + 'isch&sa=X&ved=2ahUKEwiY7bzAj8jnAhUQjq0KHbXwBEYQ_AUoAXoECBMQAw&biw=838&bih=880'

    return url
   
# Gets the HTML code of the page
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
        print("Could not get page URL!")
        sys.exit()

def get_href_from_html(raw_html):
    # Beautiful Soup Code
    soup = BeautifulSoup(raw_html, "lxml")
    # meta = tag, content = attribute
    print(soup.find(jsaction="IE7JUb:e5gl8b;MW7oTe:fL5Ibf;dtRDof:s370ud;R3mad:ZCNXMe;v03O1c:cJhY7b;").a['src'])


    # Headless browswer thing or 
    # retrieve all elements matching regular expression in beautiful soup

    # f = open("test.txt", "w")
    # f.write(soup.prettify())
    # f.close()
    

    # /html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/a[1]
    
    # tree = html.fromstring(raw_html.content)
    # href = tree.xpath('/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/a[1]')
    # print("Href:", href)







def get_thumbnail_image_url(raw_html):

    start = raw_html.find('IE7JUb:e5gl8b;MW7oTe:fL5Ibf;dtRDof:s370ud;R3mad:ZCNXMe;v03O1c:cJhY7b;')

    # start = raw_html.find('class="rg_i Q4LuWd tx8vtf"')
    if start == -1:  # If no links are found then give an error!
        end = 0
        link = "no_links"
        return link, end   
    else:
        beg_link = raw_html.find('data-tbnid="', start+1)
        end_link = raw_html.find('data-ct="', beg_link+1)
        link = str(raw_html[beg_link+12:end_link-3])
        return link, end_link


        #These lines isolate the link in the raw_html
        # beg_link = raw_html.find('data-iurl="', start+1)
        # end_link = raw_html.find('jsname="', beg_link+1)
        # link = str(raw_html[beg_link+11:end_link-2])
        # return link, end_link

def get_real_image_page(thumbnail_image_url, keyword):
    url = construct_url(keyword) + '#imgrc=' + thumbnail_image_url
    print("Modified URL: " + url)
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read()
        # string_data = data.decode('utf-8')
        # print(type(data))
        # print(type(string_data))
        # f = open("output.txt", "w+")
        # f.write(string_data)
        # f.close()
        # print(string_data.find('!doctype html><html lang="en" dir="ltr" itemscope'))
        return data
    except Exception as e:
        print("Could not get page URL")
        sys.exit()

def extract_url(real_image_page):
    # start = real_image_page.find('WtS5B:zQYYb;TgRKO:MAtQmb;agoMJf:MAtQmb;d9N7hc:MAtQmb;')
    # start2 = real_image_page.find('Image result for monkeys" class="n3VNCb"', start)
    # print(start)
    # print(start2)

    # print(real_image_page[start2:start2+50])
     # start = raw_html.find('class="rg_i Q4LuWd tx8vtf"')

    # if start2 == -1:  # If no links are found then give an error!
    #     end = 0
    #     link = "no_links"
    #     return link, end   
    # else:
    #     beg_link = real_image_page.find('src="', start2)
    #     end_link = real_image_page.find('data-noaft', beg_link)
    #     print(real_image_page[beg_link:beg_link+20])
    #     print(real_image_page[end_link-10:end_link+20])
    #     link = str(real_image_page[beg_link+5:end_link-2])
    #     return link
    print('test')
    print(type(real_image_page))
    print(real_image_page.find('Image result for donkeys'))
    return 1



# def get_image_type(start, raw_html):
#     try:
#         beg_type = raw_html.find('src="data:image/', start)
#         end_type = raw_html.find(';', beg_type+1)
#         type_of_image = str(raw_html[beg_type+16:end_type])
#         return type_of_image
#     except Exception as e:
#         print("Could not find image type")
#         sys.exit()

# def write_to_file(image_url, keyword, i):
#      try:
#          req = Request(image_url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
#          response = urlopen(req)
#          data = response.read()
#          response.close()
#          path = "Images/" + keyword + str(i) + ".jpeg" 
#          output_file = open(path, 'wb')
#          output_file.write(data)
#          output_file.close()
#      except Exception as e:
#          print("Something went wrong when downloading and saving image")


def download_images(raw_html, keyword, limit):
    sliced_html = raw_html
    for i in range(0, limit):
        #Gets Links
        thumbnail_image_url, cutoff = get_thumbnail_image_url(sliced_html)
        real_image_page = get_real_image_page(thumbnail_image_url, keyword)
        image_url = extract_url(real_image_page)
        print(image_url)
        #No links => End Program 

        # if(image_url == "no_links"):
        #     break
        # else:
        #     print("Getting thumbnail from:\t", image_url)
        #     write_to_file(image_url, keyword, i)
        #     print('\033[0;32m' + "Image", (i+1), "downloaded\n" + '\033[0m')
        #     sliced_html = sliced_html[cutoff:]
extract_url

def main():

    # Get user input
    keyword, limit = user_input()

    # Get google images URL
    url = construct_url(keyword)
    print('Got original URL: ' + url)
    print("")

    # Get the HTML of the page in the URL above
    raw_html = get_html(url)


    get_href_from_html(raw_html)

    # print('\033[1;33m' + "\nDownloading Images...\n" + '\033[0m')
    # download_images(raw_html, keyword, int(limit))
    # print('\033[1;32m' + "Download Complete\n" + '\033[0m')

if __name__ == '__main__':
    main()
