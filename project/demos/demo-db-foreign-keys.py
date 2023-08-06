import sqlite3
import requests
import datetime
from datetime import date

DB = "news.db"
ARTICLES_TABLE = "articles"
USERS_TABLE = "users"
LIKES_TABLE = "likes"

connection = sqlite3.connect(DB)
cursor = connection.cursor()

# Create articles table
def create_articles():
    cursor.execute("CREATE TABLE IF NOT EXISTS " 
        + ARTICLES_TABLE + "("
        + " id INTEGER PRIMARY KEY,"
        + " title TEXT,"
        + " author TEXT,"
        + " url TEXT," 
        + "date TEXT);"
    )
    
# Create Users table
def create_users():
    cursor.execute("CREATE TABLE IF NOT EXISTS " 
        + USERS_TABLE + "("
        + " id TEXT,"
        + " email TEXT,"
        + " name TEXT,"
        + " admin INTEGER);"
    )
    
# Create Likes table
def create_likes():
    cursor.execute("CREATE TABLE IF NOT EXISTS "
        + LIKES_TABLE + " ("
        + " user_id TEXT, "
        + " article_id INTEGER,"
        + " FOREIGN KEY(article_id)"
        + " REFERENCES articles (id));"
    )


# Initalize Articles Table
ts_url = "https://hacker-news.firebaseio.com/v0/topstories.json/"

def init_articles():
    session = requests.Session()
    ids = session.get(ts_url)
    ids_list = ids.content
    ids_list = ids_list.decode()
    ids_list = ids_list[1:-1]
    ids_list = ids_list.split(",")
    ids_list = ids_list[:50]
    articles = []
    
    for id in ids_list:
        articles.append(session.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty").json())
    
    init_date = date.today()
    init_date = init_date.strftime("%m/%d/%y")
    
    for node in articles:
        if "url" not in node:
            articles.remove(node)
            
    articles = articles[:20]
            
    for node in articles:
        cursor.execute("INSERT INTO " + ARTICLES_TABLE + " VALUES (?, ?, ?, ?, ?)",
            (node['id'], node['title'], node['by'], node['url'], init_date))
        connection.commit()
    session.close()

articles_exst = cursor.execute(
    """SELECT name FROM sqlite_master WHERE type='table'
    AND name='articles';""").fetchall()

users_exst = cursor.execute(
    """SELECT name FROM sqlite_master WHERE type='table'
    AND name='users';""").fetchall()
    
likes_exst = cursor.execute(
    """SELECT name FROM sqlite_master WHERE type='table'
    AND name='likes';""").fetchall()

if articles_exst == []:
    create_articles()
    print("[init-db]: " + ARTICLES_TABLE + " table has been created. Initalizing...")
    init_articles()
else:
    print("[init-db]: Articles table is present in database. Continuing...")

if users_exst == []:
    create_users()
    print("[init-db]: " + USERS_TABLE + " table has been created. Continuing...")
else:
    print("[init-db]: Users table is present in database. Continuing...")
    
if likes_exst == []:
    create_likes()
    print("[init-db]: " + LIKES_TABLE + " table has been created. Continuing...")
else:
    print("[init-db] Likes table is present in database. Continuing...")

connection.commit()
cursor.close()

connection.close()
print("[init-db]: Program exited.")
	
