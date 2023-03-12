from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains, ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def driver_setup():
    # Set Chrome to run in headless mode
    chrome_options = Options()
    #chrome_options.add_argument('--headless')

    # Install and manage the Chrome driver executable
    service = Service(executable_path=ChromeDriverManager().install())

    # Create a ChromeDriver instance using the installed driver executable
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL for player statistics
    stats_url = "https://fantasy.premierleague.com/statistics"

    # Navigate to a webpage
    driver.get(stats_url)
    return driver

def accept_cookies(driver):
    # Wait for the button to be clickable
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))
    )
    # Click the button
    button.click()

def find_number_of_pages(driver):
    counter = 0 #Initialize the counter to 0
    nbr_of_pages = 0 #Initialize the number of pages to 0
    while nbr_of_pages == 0:
        try:
            nbr_of_pages=driver.find_element("xpath",f'(//div[@class="sc-bdnxRM sc-gtsrHT eVZJvz gfuSqG"])/div').text # Get the number of pages
            nbr_of_pages = int(nbr_of_pages[5:7]) # Parse the number of pages to an integer
        except:
            counter += 100 # Increment the counter
            driver.execute_script(f"window.scrollTo(0,{counter});") # Scroll down the page with the counter
    return nbr_of_pages

def next_page(driver, nbr_of_pages, loop_counter):
    continue_loop = True
    while(continue_loop):
        try:
            if(loop_counter == 0):
                # Wait for the button to be clickable
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[@class='PaginatorButton__Button-xqlaki-0 cDdTXr'])"))
                )
                # Click the button
                button.click()
                # Set continue_loop to False to break out of the while loop
                continue_loop = False
            elif((loop_counter>0) and (loop_counter<nbr_of_pages-1)):
                # Wait for the button to be clickable
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[@class='PaginatorButton__Button-xqlaki-0 cDdTXr'])[2]"))
                )
                # Click the button
                button.click()
                # Set continue_loop to False to break out of the while loop
                continue_loop = False
            else:
                # Set continue_loop to False to break out of the while loop
                continue_loop = False
        except:
            # Scroll up to the top of the page
            driver.execute_script(f"window.scrollTo(0, 0);")