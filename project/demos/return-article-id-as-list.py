import sqlite3
import json

connection = sqlite3.connect("news.db")
cursor = connection.cursor()

sql = "SELECT DISTINCT article_id FROM likes"

cursor.row_factory = lambda cursor, row: row[0]
l = cursor.execute(sql).fetchall()

print(l)