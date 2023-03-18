from fpl_scraper_functions import driver_setup, find_number_of_pages, distribute_pages, loop_through_pages
import pickle

players = []

driver_1 = driver_setup(start_page=1)

nbr_of_pages_total = find_number_of_pages(driver_1)
driver_distribution = distribute_pages(nbr_of_pages_total, 5)
iteration_1 = driver_distribution[0]
loop_through_pages(driver=driver_1, nbr_of_pages_to_scrape=iteration_1, players=players, driver_name="Driver 1", \
                   nbr_of_pages_total=nbr_of_pages_total, \
                   current_page=1)
# Close the driver
driver_1.quit()

iteration_2 = driver_distribution[1]
driver_2 = driver_setup(start_page=iteration_1+1)
loop_through_pages(driver=driver_2, nbr_of_pages_to_scrape=iteration_2, players=players, \
                   driver_name="Driver 2", nbr_of_pages_total=nbr_of_pages_total, \
                   current_page=iteration_1+1)
driver_2.quit()


iteration_3 = driver_distribution[2]
driver_3 = driver_setup(start_page=iteration_1+iteration_2+1)
loop_through_pages(driver=driver_3, nbr_of_pages_to_scrape=iteration_3, players=players, \
                   driver_name="Driver 3", nbr_of_pages_total=nbr_of_pages_total, \
                   current_page=iteration_1+iteration_2+1)
driver_3.quit()

iteration_4 = driver_distribution[3]
driver_4 = driver_setup(start_page=iteration_1+iteration_2+iteration_3+1)
loop_through_pages(driver=driver_4, nbr_of_pages_to_scrape=iteration_4, players=players, \
                   driver_name="Driver 4", nbr_of_pages_total=nbr_of_pages_total, \
                   current_page=iteration_1+iteration_2+iteration_3+1)
driver_4.quit()

iteration_5 = driver_distribution[4]
driver_5 = driver_setup(start_page=iteration_1+iteration_2+iteration_3+iteration_4+1)
loop_through_pages(driver=driver_5, nbr_of_pages_to_scrape=iteration_5, players=players, \
                   driver_name="Driver 5", nbr_of_pages_total=nbr_of_pages_total, \
                   current_page=iteration_1+iteration_2+iteration_3+iteration_4+1)
driver_5.quit()

# Open a file for binary writing
with open('players.pickle', 'wb') as file:
    # Use pickle.dump() to serialize and save the list to the file
    pickle.dump(players, file)
