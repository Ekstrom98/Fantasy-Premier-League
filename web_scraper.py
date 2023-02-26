from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
    EC.element_to_be_clickable((By.XPATH, "//button[@class='_2hTJ5th4dIYlveipSEMYHH BfdVlAo_cgSVjDUegen0F js-accept-all-close']"))
)

# Click the button
button.click()
# Print the title of the page
print(driver.title)
import time 
time.sleep(4)

# Close the browser
driver.quit()