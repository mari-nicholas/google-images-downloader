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

class element_has_src(object):
  """An expectation for checking that an element has a src

  locator - used to find the element
  returns the WebElement once it has a src
  """
  def __init__(self, locator):
    self.locator = locator

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if element.get_attribute("src"):
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
   
# Gets the URL of the image
def get_image_url(url):

    # Setting chrome options, specifically headless (runs without visual browswer)
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = '/usr/bin/google-chrome'

    # Create a chrome webdriver
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),   chrome_options=chrome_options) 
    # driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"))

    driver.get(url)

    # Find and click on the first image thumbnail
    image_thumbnail = driver.find_elements_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/a[1]")
    image_thumbnail[0].click()

    # https://selenium-python.readthedocs.io/waits.html#explicit-waits, https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions
    # image = WebDriverWait(driver, 10).until(element_has_src((By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img")))
    # print(image.get_attribute("class"))
    # image_url = image.get_attribute("src")

    time.sleep(1) #Instead of waiting for a specified time, can just wait for a specific element to load. Add later

    # Find the full image and get its URL embedded in the html
    image = driver.find_elements_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img")
    image_url = image[0].get_attribute("src")

    # Quit the driver
    driver.quit()

    # Return the image URL
    return image_url


# Downloads the image
def download_images(image_url, keyword):

    print("Getting image from: ", image_url)

    try:
         req = Request(image_url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
         response = urlopen(req)
         data = response.read()
         response.close()
         path = "Images/" + keyword
         output_file = open(path, 'wb')
         output_file.write(data)
         output_file.close()
         print('\033[0;32m' + "Image downloaded\n" + '\033[0m')

    except Exception as e:
         print("Something went wrong when downloading and saving image")

def main():

    # Get user input
    keyword, limit = user_input()

    # Get google images search querry URL
    url = construct_url(keyword)
    print('URL with all image thumbnails: ' + url)
    print("")

    # Get the URL of the image
    image_url = get_image_url(url)

    # Download the images
    print('\033[1;33m' + "Downloading Images...\n" + '\033[0m')
    download_images(image_url, keyword)
    print('\033[1;32m' + "Download Complete\n" + '\033[0m')

if __name__ == '__main__':
    main()
