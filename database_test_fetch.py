import sqlite3
# connect to the database
conn = sqlite3.connect('players.db')

# create a cursor object to execute SQL queries
c = conn.cursor()

# fetch and print all rows
c.execute("SELECT * FROM players_table")
print(c.fetchall())

# close the cursor and connection
c.close()
conn.close()
