###
#
# update-db.py
#
# description:
#
# maintained by:
# Carlos Pantoja-Malaga
# Matthew Kolnicki
#
###
import requests
import sqlite3
import datetime
import json

db = "news.db"
articles_table = "articles"

connection = sqlite3.connect(db)
cursor = connection.cursor()

ts_url = "https://hacker-news.firebaseio.com/v0/topstories.json/"

def snag_articles():
    session = requests.Session()
    ids = session.get(ts_url)
    ids_list = ids.content
    ids_list = ids_list.decode()
    ids_list = ids_list[1:-1]
    ids_list = ids_list.split(",")
    ids_list = ids_list[25:]
    
    print("------------------------------")
    print("POTENTIAL IDS: SIZE: " + str(len(ids_list)))
    print(ids_list)
    print("------------------------------")
    
    cursor.execute("SELECT id FROM articles")
    cursor.row_factory = lambda cursor, row: row[0]
    stored = cursor.fetchall()
    print("------------------------------")
    print("STORED IDS: SIZE: " + str(len(stored)))
    print(stored)
    print("------------------------------")
    
    i = 0
    size = len(stored)
    
    for id in ids_list:
        if int(id) in stored:
            continue
        else:
            stored.append(int(id))
        if size < (size + 5):
            i+=1
        if i == 5:
            break
    
    articles = []
    
    print("------------------------------")
    print("STORED IDS + NEW IDS: SIZE: " + str(len(stored)))
    print(stored)
    print("------------------------------")
    
    print("------------------------------")
    big = stored[-5:]
    print("EXPECTED NEW IDS: SIZE: " + str(len(big)))
    print(big)
    print("------------------------------")
    
    for id in big:
        articles.append(session.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty").json())
    
    valid_articles = []
    for key in articles:
        if "url" in key:
            valid_articles.append(key)
    
    print("------------------------------")
    print("ACTUAL VALID IDS BEING PUT IN DATABASE")
    print(json.dumps(valid_articles, indent=4))
    print("------------------------------")
    
    init_date = datetime.datetime.now()
    
    for node in valid_articles:
        cursor.execute("INSERT OR IGNORE INTO " + articles_table + " VALUES (?, ?, ?, ?, ?)",
            (node['id'], node['title'], node['by'], node['url'], init_date))
            
    connection.commit()
    session.close()

snag_articles()
cursor.close()
connection.close()
print("[update-db]: Updated & exited.")
