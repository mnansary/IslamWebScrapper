#-*- coding: utf-8 -*-
from __future__ import print_function
# ---------------------------------------------------------
# imports
# ---------------------------------------------------------
import random
from time import sleep

# web driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# ---------------------------------------------------------
# browser
# ---------------------------------------------------------
driver=None
old_height=0



def launchBrowser(Debug=False):
    '''
        Browser options
    '''
    
    global driver

    options = Options()
    prefs = {'profile.default_content_setting_values': {'images': 2}}
    options.add_experimental_option('prefs', prefs)
    
    # Code to disable notifications pop up of Chrome Browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    
    if not Debug:
        options.add_argument("--headless")
    
    try:
        # Correct way to use the webdriver manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Error launching browser: {e}")
    
    return driver



# ---------------------------------------------------------
def check(element, xpath):
    '''
    Checks if an element exists by XPath.
    '''
    try:
        element.find_element(By.XPATH, xpath)
        return True
    except NoSuchElementException:
        return False

def waitSomeTime(mult=None):
    '''
    Waits a random amount of time (between 1 and 3 seconds) to mimic human behavior.
    '''
    _wait_time = round(random.random() * 2 + 1, 2)

    if mult is None:
        sleep(_wait_time)
    else:
        for _ in range(mult):
            sleep(_wait_time)

# ---------------------------------------------------------
def scrollCheckHeight(driver):
    '''
    Check if page height has changed after scrolling.
    '''
    global old_height
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height

def scroll(driver):
    '''
    Scrolls the page to the bottom and waits for new content to load.
    '''
    global old_height
    try:
        old_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait until the height changes, indicating that the scroll is complete
        WebDriverWait(driver, 10, 0.05).until(lambda x: scrollCheckHeight(driver))
    except TimeoutException:
        print("Scroll timeout or page height didn't change.")
    except Exception as e:
        print(f"Error during scrolling: {e}")

# ---------------------------------------------------------
def clickLink(link):
    '''
    Clicks a link. If a direct click fails, it tries using JavaScript.
    '''
    try:
        # Try direct click
        link.click()
    except Exception as e1:
        try:
            # Fallback to JavaScript click
            driver.execute_script("arguments[0].click();", link)
        except Exception as e2:
            print(f"Failed to click link: {e2}")
