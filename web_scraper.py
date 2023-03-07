from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains, ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Wait for the button to be clickable
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))
)
# Click the button
button.click()

player_batch = []
all_players = []


counter = 0
nbr_of_pages = 0
while nbr_of_pages == 0:
    try:
        nbr_of_pages=driver.find_element("xpath",f'(//div[@class="sc-bdnxRM sc-gtsrHT eVZJvz gfuSqG"])/div').text
        nbr_of_pages = int(nbr_of_pages[5:7])
    except:
        counter += 10
        driver.execute_script(f"window.scrollTo(0,{counter});")
        



for j in range(nbr_of_pages):
    counter = 0
    driver.execute_script("window.scrollTo(0,0);")
    nbr_of_elements = len(driver.find_elements("xpath",'//div[@class="ElementInTable__Name-y9xi40-1 heNyFi"]'))
    
    for i in range(nbr_of_elements):
        try:
            element = driver.find_element("xpath",f'(//div[@class="ElementInTable__Name-y9xi40-1 heNyFi"])[{i+1}]').text
            player_batch.append(element)
        except:
            counter += 100
            driver.execute_script(f"window.scrollTo(0, {counter});")

    while(len(player_batch) == nbr_of_elements):
        try:
            if(j == 0):
                # Wait for the button to be clickable
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[@class='PaginatorButton__Button-xqlaki-0 cDdTXr'])"))
                )
                # Click the button
                button.click()
                nbr_of_elements = 0
            elif((j>0) and (j<nbr_of_pages-1)):
                # Wait for the button to be clickable
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[@class='PaginatorButton__Button-xqlaki-0 cDdTXr'])[2]"))
                )
                # Click the button
                button.click()
                nbr_of_elements = 0
            else:
                 nbr_of_elements = -1
        except:
            print("esaea")
            pass
    
    all_players.append(player_batch)
    player_batch = []
    if(j == nbr_of_pages - 1):
        print("Scraper finished.")
        break

# Close the browser
driver.quit()
