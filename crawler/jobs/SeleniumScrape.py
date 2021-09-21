# **************************************************************
# MAINTENANCE BOX
# 10.10: Ben O'Brien created the selenium file, refer description below
# 10.10: Ben O'Brien created the functionality to open the search, locate the appropriate page and click
# 10.10: Ben O'Brien created the functionality to take a page input and return the raw HTML of that page
# **************************************************************

# NOTE: This file is not currently being used. It was the initial solution to scraping additional page results
# from career one which are generated client side.
# As selenium is not supported on Azure, we have found an alternative workaround.
# Although this file is not being used it still represents completed work so leaving it here for records.

# This file is used to run Selenium which allows scraping to be completed by clicking links on pages.
# CareerOne displays paginated results in a single page view i.e. the URL does not change when the NEXT
# page is viewed.
# These types of pages cannot be scraped with BeautifulSoup.
# Selenium will be used to click 'NEXT' and scrape the updated page

# REFERENCE: Selenium scraping functionality is based on the scrapingbee article
# https://www.scrapingbee.com/blog/selenium-python/

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class SeleniumScrape():

    def __init__(self, url):
        #class attributes
        self._DRIVER_PATH = 'chromedriver.exe'
        self._url = url

        #selenium options
        self._options = Options()
        self._options.headless = True
        self._options.add_argument("--window-size=1920,1200")

    #function to find the appropriate page number, open it and return the page html
    def scrape(self, pageNum):

        #page html will be stored in soup variable
        soup = None
        #open the specified URL in the driverless browser
        driver = webdriver.Chrome(options=self._options, executable_path=self._DRIVER_PATH)
        driver.get(self._url)
        #find the pagination bar
        target = driver.find_element_by_class_name('pagination')
        #create a list of all the buttons in the pagination bar
        all_buttons = target.find_elements_by_tag_name('button')
        #store the current window
        window_before = driver.window_handles[0]
        for item in all_buttons:
            if item.text == str(pageNum):
                item.click()

                #wait 5 seconds to allow the page to load
                time.sleep(5)
                #switch the driver to the new window
                new_window = driver.current_window_handle
                driver.switch_to_window(new_window)
                soup = driver.find_element_by_xpath('//html').get_attribute('outerHTML')

        #close web page
        driver.quit()

        return soup
