from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains, ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from fpl_scraper_functions import driver_setup, accept_cookies, find_number_of_pages, next_page, open_extended_player_info, this_season_stats, close_extended_player_info

driver = driver_setup()

accept_cookies(driver)
nbr_of_pages = find_number_of_pages(driver)
players = []

# Loop through the pages
for j in range(nbr_of_pages):
    os.system('clear') # Clear the terminal
    percentage_done = (j+1)/nbr_of_pages*100 # Calculate the percentage of pages done
    print(f"Scraper is on page {j+1} of {nbr_of_pages} ({percentage_done}% done).") # Print the current page number and the progress in %

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

    # Go to the next page
    next_page(driver, nbr_of_pages,loop_counter=j)

    if(j == nbr_of_pages - 1):
        print("Scraper is finished.")
        break

# Close the browser
driver.quit()