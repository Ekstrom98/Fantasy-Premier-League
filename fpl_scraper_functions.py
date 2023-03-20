from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains, ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.common.exceptions import TimeoutException



def driver_setup(start_page: int = 1):
    # Set Chrome to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    # Install and manage the Chrome driver executable
    service = Service(executable_path=ChromeDriverManager().install())

    # Create a ChromeDriver instance using the installed driver executable
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL for player statistics
    stats_url = "https://fantasy.premierleague.com/statistics"
    
    # Navigate to a webpage
    driver.get(stats_url)
    accept_cookies(driver)
    nbr_of_pages=find_number_of_pages(driver)
    
    if(start_page>1):
        next_page_driver_setup(driver, start_page-1, nbr_of_pages)
    driver.execute_script(f"window.scrollTo(0, 0);")
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

def next_page_driver_setup(driver, start_page, nbr_of_pages):
    loop_counter = 0
    for i in range(start_page):
        counter = 0
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
                    loop_counter += 1
                elif((loop_counter>0) and (loop_counter<nbr_of_pages-1)):
                    # Wait for the button to be clickable
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "(//button[@class='PaginatorButton__Button-xqlaki-0 cDdTXr'])[2]"))
                    )
                    # Click the button
                    button.click()
                    # Set continue_loop to False to break out of the while loop
                    continue_loop = False
                    loop_counter += 1
                else:
                    # Set continue_loop to False to break out of the while loop
                    continue_loop = False
            except:
                # If an error occurs, scroll down the page and try again
                counter += 100
                driver.execute_script(f"window.scrollTo(0, {counter});")

def next_page(driver, nbr_of_pages, current_page):
    continue_loop = True
    while(continue_loop):
        try:
            if(current_page == 1):
                # Wait for the button to be clickable
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[@class='PaginatorButton__Button-xqlaki-0 cDdTXr'])"))
                )
                # Click the button
                button.click()
                # Set continue_loop to False to break out of the while loop
                continue_loop = False

            elif(current_page > 1 and current_page < nbr_of_pages - 1):
                # Wait for the button to be clickable
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[@class='PaginatorButton__Button-xqlaki-0 cDdTXr'])[2]"))
                )
                # Click the button
                button.click()
                # Set continue_loop to False to break out of the while loop
                continue_loop = False

            else:
                try:
                    # Wait for the button to be clickable
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "(//button[@class='PaginatorButton__Button-xqlaki-0 cDdTXr'])[2]"))
                    )
                    # Click the button
                    button.click()
                finally:
                    # Set continue_loop to False to break out of the while loop
                    continue_loop = False
        except:
            # Scroll up to the top of the page
            driver.execute_script(f"window.scrollTo(0, 0);")
            pass

def open_extended_player_info(driver, loop_counter=None):

    # Wait for the button to be clickable
    info_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, \
                        f'(//button[@class="ElementDialogButton__StyledElementDialogButton-sc-1vrzlgb-0 jVAeGl"])[{loop_counter+1}]'))
    )
    # Click the button
    info_button.click()

def close_extended_player_info(driver):
    close_button_xpath = '//button[@class="Dialog__CloseButton-sc-5bogmv-1 cgQMVU"]'
    # Wait for the button to be clickable
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, close_button_xpath))
    )
    # Click the button
    close_button.click()

def this_season_stats(driver):
    super_css="#root-dialog > div > dialog > div > div.Dialog__StyledDialogBody-sc-5bogmv-9.jyKAwP.ism-overflow-scroll"
    # Define the locator for the element you want to wait for
    element_locator = (By.CSS_SELECTOR, "tr.styles__HistoryTotalsRow-ahs9zc-18.jZiieB")

    # Set the maximum time you want to wait for the element (in seconds)
    timeout = 10

    try:
        # Wait for the element to be visible
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(element_locator)
        )
        # Perform actions with the element here
        print("Element is visible now.")
        
    except TimeoutException:
        print(f"Element with locator {element_locator} not visible after {timeout} seconds.")

    all_player_info = driver.find_element("css selector", super_css).text

    return all_player_info

def distribute_pages(nbr_of_pages, sections):
    result = [0] * sections
    for i in range(nbr_of_pages):
        result[i % sections] += 1
    return result

def loop_through_pages(driver, nbr_of_pages_to_scrape:int, players:list, nbr_of_pages_total: int, driver_name = None, current_page = 1):
    driver_name = driver_name
    # Loop through the pages
    for j in range(nbr_of_pages_to_scrape):
        os.system('clear') # Clear the terminal
        print(f"{driver_name} is on page {j+1} of {nbr_of_pages_to_scrape}.") # Print the current page number and the progress in %

        counter = 0 # Reset the counter
        driver.execute_script("window.scrollTo(0,0);") # Scroll up to the top of the page

        # Find the number of players on the page
        nbr_of_elements = len(driver.find_elements("xpath",'//div[@class="ElementInTable__Name-y9xi40-1 heNyFi"]'))

        # Loop through the players on the page
        for i in range(nbr_of_elements):
            # Try to find the player data
            information_fetched = False
            while(information_fetched == False):
                try:
                    open_extended_player_info(driver = driver, loop_counter = i)
                    player_info = this_season_stats(driver = driver)
                    players.append(player_info)
                    information_fetched = True
                except:
                    # If an error occurs, scroll down the page and try again
                    counter += 100
                    driver.execute_script(f"window.scrollTo(0, {counter});")
        
            # Close the extended player info
            close_extended_player_info(driver = driver)
        next = True
        while(next):
            counter = 0
            try:
                # Go to the next page
                next_page(driver, nbr_of_pages_total,current_page=j+current_page)
                next = False
            except:
                counter += 1
                print("Failure to go to next page. Trying again.")
                if(counter == 10):
                    print("Too many failures. Exiting.")
                    break
        if(j == nbr_of_pages_to_scrape - 1):
            print("Scraper is finished.")
            break