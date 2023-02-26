import requests 
from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio

stats_url = "https://fantasy.premierleague.com/statistics"
response_1 = requests.get(stats_url)

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(stats_url)
    # Scrape content here
    response_2 = requests.get(stats_url)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
