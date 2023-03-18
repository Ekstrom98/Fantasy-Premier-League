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
from fpl_scraper_functions import distribute_pages, loop_through_pages
import pickle

driver_1 = driver_setup(start_page=1)
nbr_of_pages = find_number_of_pages(driver_1) 

players = []
driver_distribution = distribute_pages(nbr_of_pages, 5)
iteration_1 = driver_distribution[0]
iteration_2 = driver_distribution[1]
iteration_3 = driver_distribution[2]
iteration_4 = driver_distribution[3]
iteration_5 = driver_distribution[4]

driver_2 = driver_setup(start_page=iteration_1+1)
driver_3 = driver_setup(start_page=iteration_1+iteration_2+1)
driver_4 = driver_setup(start_page=iteration_1+iteration_2+iteration_3+1)
driver_5 = driver_setup(start_page=iteration_1+iteration_2+iteration_3+iteration_4+1)

loop_through_pages(driver=driver_1, nbr_of_pages=iteration_1, players=players)
loop_through_pages(driver=driver_2, nbr_of_pages=iteration_2, players=players)
loop_through_pages(driver=driver_3, nbr_of_pages=iteration_3, players=players)
loop_through_pages(driver=driver_4, nbr_of_pages=iteration_4, players=players)
loop_through_pages(driver=driver_5, nbr_of_pages=iteration_5, players=players)




# Open a file for binary writing
with open('players.pickle', 'wb') as file:
    # Use pickle.dump() to serialize and save the list to the file
    pickle.dump(players, file)

