import sqlite3
import pandas as pd

connection = sqlite3.connect("news.db")
cursor = connection.cursor()

a_id = ""
u_id = ""
sql = "SELECT id FROM likes WHERE article_id='" + a_id + "' AND user_id='" + u_id + "';"

ex = cursor.execute(sql).fetchall();

if ex == []:
    print("empty")
else:
    print(ex)
    print("somethin aint workin chief this table should be empty")