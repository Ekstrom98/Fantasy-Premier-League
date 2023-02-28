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
chrome_options.add_argument('--headless')

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
    EC.element_to_be_clickable((By.XPATH, "//button[@class='_2hTJ5th4dIYlveipSEMYHH BfdVlAo_cgSVjDUegen0F js-accept-all-close']"))
)
# Click the button
button.click()

player_list = []
import time
element = driver.find_element("xpath",'//*[@id="root"]/div[2]/div/div[1]/table/tbody/tr[1]').text
nbr_of_elements = len(driver.find_element("xpath",'//*[@id="root"]/div[2]/div/div[1]/table/tbody/tr').text)

counter = 0
for i in range(nbr_of_elements):
    try:
        element = driver.find_element("xpath",f'//*[@id="root"]/div[2]/div/div[1]/table/tbody/tr[{i+1}]').text
        player_list.append(element)
        print(player_list)
    except:
        counter += 100
        driver.execute_script(f"window.scrollTo(0, {counter});")

# Close the browser
driver.quit()