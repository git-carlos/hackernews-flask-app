###
#
# promote.py
#
# description:
# updates admin value for user id present in administrators.txt
#
# maintained by:
# Carlos Pantoja-Malaga
# Matthew Kolnicki
#
###
import sqlite3

# parse file containing 1 id per line
file = open('administrators.txt', 'r')
contents = file.read().splitlines()

# establish database connection
db = "news.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()

# for each user id in the file, update their admin value to 1 to set role as administrator
for user in contents:
    query = cursor.execute("UPDATE users SET admin=1 WHERE id=?", (user,))

# commit changes and end session
connection.commit()
cursor.close()
connection.close()

# inform of promoted ids
for user in contents:
    print("Promoted id #: " + user + " to administrator")
