## @file NavigatePage.py
#  @author Joshua Guinness, Samuel Crawford
#  @brief Provides the functionality for getting the image URLs to download
#  @date 03/31/2020

from os import path
from platform import system
from re import search

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


## @brief Helper class to determine whether 
# element is loaded correctly
#  @details makes selenium wait until src
#  element in HTML has http and is not
#  https://encrypted. This ensures that an
#  actual image URL is added to the list
#  @param object HTML element
#  @return The URL in the src if it exists
class ElementHasSrc(object):
    """An expectation for checking that an element has a src with regex: http*

    locator - used to find the element
    returns the WebElement once it has a src with regex: http*
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        # Finding the referenced element
        element = driver.find_element(*self.locator)
        if (element.get_attribute("src")[0:4] == "http") and \
           (element.get_attribute("src")[0:17] != "https://encrypted"):
            return element
        else:
            return False


## @brief gets the image URLs
#  @details Uses selenium to open up the search
#  query URL and then navigate to each individual
#  image to get its URL and adding it to a list
#  @param url search query URL
#  @param limit number of images to get
#  @param blacklist site to blacklist in Google search
#  @return urls list of image urls to download
def getImageURL(url, limit, blacklist):

    if (limit <= 0):
        raise ValueError("Limit must be greater than 0")

    # Setting chrome options, headless = runs without visual browswer
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Options for different platforms
    plt = system().lower()
    if plt == "windows":
        chrome_options.binary_location = \
            path.join("C:\\Program Files (x86)", "Google", "Chrome",
                      "Application", "chrome.exe")
        chromeDriver = "chromedriver-win.exe"

    elif plt == "linux":
        chrome_options.binary_location = \
            path.join("/usr", "bin", "google-chrome")
        chromeDriver = "chromedriver-linux"

    elif plt == "darwin":
        chrome_options.binary_location = \
            path.join("/Applications", "Google\\ Chrome.app", "Contents",
                      "MacOS", "Google\\ Chrome")
        chromeDriver = "chromedriver-mac"

    else:
        raise Exception("Your OS is not supported")

    # Remove options for visual browser
    driver = webdriver.Chrome(executable_path=path.abspath(chromeDriver),
                              options=chrome_options)

    urls = []
    i = 0

    print('\033[38;2;244;208;63m' +
          "\nGetting the image URLs, please be patient." +
          '\033[0m')

    # While loop which iterates until the limit #
    # of images has been added the list
    while len(urls) < limit:

        print("Getting image #" + str(i + 1))

        try:
            # Get the URL
            driver.get(url)

            # Find and click on the first image thumbnail
            image_thumbnail = driver.find_elements_by_xpath(
                "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/\
                    div/div/div[1]/div[1]/div[" + str(i + 1) + "]/a[1]")
            image_thumbnail[0].click()

            # Wait until a specific element has loaded that
            # matches the regex: src = "http*"
            # https://selenium-python.readthedocs.io/waits.html#explicit-waits
            # https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions
            image = WebDriverWait(driver, 4).until(ElementHasSrc(
                (By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/\
                    div[3]/div/div/div[3]/div[2]/div/div[1]/div[1]/\
                        div/div[2]/a/img")))
            # Get what is in the src attribute. This is the full image URL
            image_url = image.get_attribute("src")

            # If not blacklist, simply add image URL to list
            if (blacklist == ""):
                urls.append(image_url)
            # If blacklist, then confirm that the blacklist
            # is not present in the image URL
            else:
                # Regex search
                result = search(blacklist, image_url)
                if result is None:
                    urls.append(image_url)
                else:
                    print("\033[38;2;255;0;0mError: Blacklisted Image " +
                          str(i + 1) + '\033[0m')

        except Exception:
            print("\033[38;2;255;0;0mError: Could not get image " +
                  str(i + 1) + '\033[0m')

        i += 1

    # Quit the driver
    driver.quit()

    # Return the list of image URLs
    return urls
