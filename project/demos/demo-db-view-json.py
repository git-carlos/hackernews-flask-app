import sqlite3
import json
import requests

# interacting with database
connection = sqlite3.connect('articles.db')
cursor = connection.cursor()

def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stored(
        id INTGER,
        title TEXT,
        author TEXT,
        url TEXT
    )""")

# Top Stories URL
ts_url = "https://hacker-news.firebaseio.com/v0/topstories.json/"

def json_construct():
    sesh = requests.Session()
    ids = sesh.get(ts_url)
    ids_list = ids.content
    ids_list = ids_list.decode()
    ids_list = ids_list[1:-1]
    ids_list = ids_list.split(",")
    ids_list = ids_list[:20]
    articles = []
    
    for id in ids_list:
        articles.append(sesh.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty").json())
    
    big = json.dumps(articles, indent=4)
    print(big)
    sesh.close()

create_table()
json_construct()
