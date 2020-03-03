from lxml import html
from bs4 import BeautifulSoup
import requests
import sys
import urllib.request
from urllib.request import Request, urlopen

# Gets the image URL
def main():
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request("https://www.google.com/imgres?imgurl=https%3A%2F%2Fcdn.mos.cms.futurecdn.net%2F6h8C6ygTdR2jyyUxkALwsc-320-80.jpg&imgrefurl=https%3A%2F%2Fwww.livescience.com%2F54258-donkeys.html&tbnid=rgr8UZ_nc6G_HM&vet=12ahUKEwiBlJbVkP_nAhVd_6wKHRJ8DkkQMygAegUIARCKAg..i&docid=NvtDSdTmwQ5hWM&w=320&h=213&q=donkeys&ved=2ahUKEwiBlJbVkP_nAhVd_6wKHRJ8DkkQMygAegUIARCKAg", headers=headers)
        response = urllib.request.urlopen(req)
        data = str(response.read())
    except Exception as e:
        print("Could not get page URL")
        sys.exit()

    # Beautiful Soup Code
    soup = BeautifulSoup(data, "lxml")
    print(soup.meta['content'])

if __name__ == '__main__':
    main()