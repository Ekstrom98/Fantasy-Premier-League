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

# Set Chrome to run in headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')

# Install and manage the Chrome driver executable
service = Service(executable_path=ChromeDriverManager().install())

# Create a ChromeDriver instance using the installed driver executable
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL for player statistics
stats_url = "https://fantasy.premierleague.com/statistics"

# connect to the database
conn = sqlite3.connect('players.db')

# create a cursor object to execute SQL queries
c = conn.cursor()

# execute a SQL query to create a table
c.execute('''CREATE TABLE IF NOT EXISTS players_table
             (id INTEGER PRIMARY KEY, name TEXT, cost REAL, selected_by TEXT, form REAL, points INTEGER, team TEXT)''')

# Navigate to a webpage
driver.get(stats_url)

# Wait for the button to be clickable
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))
)
# Click the button
button.click()

counter = 0 #Initialize the counter to 0
nbr_of_pages = 0 #Initialize the number of pages to 0
while nbr_of_pages == 0:
    try:
        nbr_of_pages=driver.find_element("xpath",f'(//div[@class="sc-bdnxRM sc-gtsrHT eVZJvz gfuSqG"])/div').text # Get the number of pages
        nbr_of_pages = int(nbr_of_pages[5:7]) # Parse the number of pages to an integer
    except:
        counter += 100 # Increment the counter
        driver.execute_script(f"window.scrollTo(0,{counter});") # Scroll down the page with the counter

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
            
            # Insert player data into the 'players_table' table
            c.execute("INSERT INTO players_table (name, cost, selected_by, form, points, team) \
           VALUES (?, ?, ?, ?, ?, ?)", (player_name, player_cost, player_selected_by, player_form, player_points, player_team))
            # Commit the changes to the database
            conn.commit()
        # If an error occurs, scroll down the page and try again
        except:
            counter += 100
            driver.execute_script(f"window.scrollTo(0, {counter});")

    continue_loop = True
    while(continue_loop):
        try:
            if(j == 0):
                # Wait for the button to be clickable
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[@class='PaginatorButton__Button-xqlaki-0 cDdTXr'])"))
                )
                # Click the button
                button.click()
                # Set continue_loop to False to break out of the while loop
                continue_loop = False
            elif((j>0) and (j<nbr_of_pages-1)):
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

    if(j == nbr_of_pages - 1):
        print("Scraper finished.")
        break
    
# Close the cursor and the database connection
c.close()
conn.close()

# Close the browser
driver.quit()