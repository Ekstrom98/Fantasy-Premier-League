from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains, ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sqlite3
from fpl_scraper_functions import driver_setup, accept_cookies, find_number_of_pages, next_page

driver = driver_setup()

accept_cookies(driver)
nbr_of_pages = find_number_of_pages(driver)

# Loop through the pages
for j in range(nbr_of_pages):
    os.system('clear') # Clear the terminal
    print(f"Scraper is on page {j+1} of {nbr_of_pages}.") # Print the current page number

    counter = 0 # Reset the counter
    driver.execute_script("window.scrollTo(0,0);") # Scroll up to the top of the page

    # Find the number of players on the page
    nbr_of_elements = len(driver.find_elements("xpath",'//div[@class="ElementInTable__Name-y9xi40-1 heNyFi"]'))#

    # Loop through the players on the page
    for i in range(nbr_of_elements):
        # Try to find the player data
        try:
            player_name = driver.find_element("xpath",f'(//div[@class="ElementInTable__Name-y9xi40-1 heNyFi"])[{i+1}]').text
            player_cost = driver.find_element("xpath",f'(//tr[@class="ElementTable__ElementRow-sc-1v08od9-3 kGMjuJ"])[{i+1}]/td[3]').text
            player_selected_by = driver.find_element("xpath",f'(//tr[@class="ElementTable__ElementRow-sc-1v08od9-3 kGMjuJ"])[{i+1}]/td[4]').text
            player_form = driver.find_element("xpath",f'(//tr[@class="ElementTable__ElementRow-sc-1v08od9-3 kGMjuJ"])[{i+1}]/td[5]').text
            player_points = driver.find_element("xpath",f'(//tr[@class="ElementTable__ElementRow-sc-1v08od9-3 kGMjuJ"])[{i+1}]/td[6]').text
            player_team = driver.find_element("xpath",f'(//span[@class="ElementInTable__Team-y9xi40-3 hosEuf"])[{i+1}]').text
            
        # If an error occurs, scroll down the page and try again
        except:
            counter += 100
            driver.execute_script(f"window.scrollTo(0, {counter});")

    next_page(driver, nbr_of_pages,loop_counter=j)

    if(j == nbr_of_pages - 1):
        print("Scraper is finished.")
        break

# Close the browser
driver.quit()