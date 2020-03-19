# Secrets: The layout of the Google search page.
# Services: Uses the processed Google search query to obtain the URL of each individual image.

from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
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

def getImageURL(url, limit):

    # Setting chrome options, specifically headless (runs without visual browswer)
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = '/usr/bin/google-chrome' # Needs to change depending on OS

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
