import sqlite3
import requests
import datetime

db = "news.db"
articles_tables = "articles"
users_table = "users"
likes_table = "likes"
dislikes_table = "dislikes"

connection = sqlite3.connect(db)
cursor = connection.cursor()


# commit and exit
connection.commit()
cursor.close()
connection.close()
print("[init-db] Program exited.")