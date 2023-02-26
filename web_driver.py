from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


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

# Print the title of the page
print(driver.title)

# Close the browser
driver.quit()