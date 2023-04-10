import requests
import sqlite3
import datetime
import json

db = "news.db"
articles_table = "articles"

connection = sqlite3.connect(db)
cursor = connection.cursor()

TSURL ="https://hacker-news.firebaseio.com/v0/topstories.json/"

cursor.close()
connection.close()
print("[update-db]: Program exited.")