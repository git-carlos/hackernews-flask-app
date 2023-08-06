
import sqlite3

USERS_TABLE = "users"

DB = "news.db"
connection = sqlite3.connect(DB)
cursor = connection.cursor()

id = "google-oauth2|112097886750082028328"

# check admin val
val = cursor.execute("SELECT admin FROM users WHERE id='" + id + "';").fetchone()

# returning a tuple wow! must fix and make integer!
val = int(val[0])

print(val)
