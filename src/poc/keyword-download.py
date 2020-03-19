import argparse
import sys
import urllib.request
import requests
from urllib.parse import quote
from urllib.request import Request, urlopen
from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import re
import os
import time

# Helper function to determine whether element is loaded correctly
class element_has_src(object):
  """An expectation for checking that an element has a src with regex: http*

  locator - used to find the element
  returns the WebElement once it has a src with regex: http*
  """
  def __init__(self, locator):
    self.locator = locator

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if element.get_attribute("src")[0:4] == "http":
        return element
    else:
        return False

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
   
# Gets a list of the image URLs
def get_image_urls(url, limit):

    # Setting chrome options, specifically headless (runs without visual browswer)
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = '/usr/bin/google-chrome'

    # Create a chrome webdriver
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),   chrome_options=chrome_options) # Headless
    # driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver")) # Not Headless (With Visual Chrome)

    urls = []
    numberOfImages = int(limit)
    i = 0

    print('\033[38;2;0;0;255m' + "Getting the image URLs, please be patient this may take some time." + '\033[0m')

    while i < numberOfImages:

        try:
            # Get the URL
            driver.get(url)

            # Find and click on the first image thumbnail
            image_thumbnail = driver.find_elements_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[" + str(i+1) + "]/a[1]")
            image_thumbnail[0].click()

            # Wait until a specific element has loaded that matches the regex: src = "http*"
            # https://selenium-python.readthedocs.io/waits.html#explicit-waits, https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions
            image = WebDriverWait(driver, 2).until(element_has_src((By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img")))
            # Get what is in the src attribute. This is the full image URL
            image_url = image.get_attribute("src")

            urls.append(image_url)

            i += 1

        except Exception as e:
            # https://askubuntu.com/questions/801299/change-text-color-of-my-output-on-command-prompt
            print('\033[38;2;255;0;0m' + "Error: Could not get image " + str(i+1) + '\033[0m')
            
            # Since could not download this image, extend the range by one so the correct number of images
            # are still downloaded.
            numberOfImages += 1
            i += 1

    # Quit the driver
    driver.quit()

    # Return the list of image URLs
    return urls


# Downloads the image
def download_images(image_urls, keyword):

    print("Number of images to download:", '\033[1;32m' + str(len(image_urls)) + '\033[0m')

    for i in image_urls:
        print(i)

    # for i in image_urls:
    #     print("Getting image from:", i)

    #     try:
    #         req = Request(i, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
    #         response = urlopen(req)
    #         data = response.read()
    #         response.close()
    #         path = "Images/" + keyword
    #         output_file = open(path, 'wb')
    #         output_file.write(data)
    #         output_file.close()
    #         print('\033[0;32m' + "Image downloaded\n" + '\033[0m')

    #     except Exception as e:
    #         print("Something went wrong when downloading and saving image")

def main():

    # Get user input
    keyword, limit = user_input()

    # Get google images search querry URL
    url = construct_url(keyword)
    print('\nURL with all image thumbnails: ' + url)
    print("")

    # Get the URL of the image
    image_urls = get_image_urls(url, int(limit))

    print(image_url)

    # Download the images
    print('\n\033[1;33m' + "Downloading Images...\n" + '\033[0m')
    download_images(image_urls, keyword)
    print('\n\033[1;32m' + "Download Complete!\n" + '\033[0m')

if __name__ == '__main__':
    main()
