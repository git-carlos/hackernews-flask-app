###
#
# init-db.py
#
# description:
# creates database tables necessitated for web application to function
# intializes articles table with initial article data
# should be run on startup to ensure database has necessitated tables
#
# maintained by:
# Carlos Pantoja-Malaga
# Matthew Kolnicki
#
###
import sqlite3
import requests
import datetime

# naming convention
db = "news.db"
articles_table = "articles"
users_table = "users"
likes_table = "likes"
dislikes_table = "dislikes"

# establish database connection
connection = sqlite3.connect(db)
cursor = connection.cursor()

# create articles table with schema: id, title, author, url, date
def create_articles():
    cursor.execute("CREATE TABLE IF NOT EXISTS " 
        + articles_table + "( "
        + "id INTEGER PRIMARY KEY, "
        + "title TEXT, "
        + "author TEXT, "
        + "url TEXT, " 
        + "date TIMESTAMP, " 
        + "UNIQUE(id, title));"
    )
    
# create users table with schema: id, email, name, admin
def create_users():
    cursor.execute("CREATE TABLE IF NOT EXISTS " 
        + users_table + "("
        + "id TEXT, "
        + "email TEXT, "
        + "name TEXT, "
        + "admin INTEGER);"
    )
    
# create likes table with schema: id(user), id(article)
def create_likes():
    cursor.execute("CREATE TABLE IF NOT EXISTS "
        + likes_table + " ("
        + " user_id TEXT, "
        + " article_id INTEGER,"
        + " FOREIGN KEY(article_id)"
        + " REFERENCES articles (id));"
    )

# create likes table with schema: id(user), id(article)
def create_dislikes():
    cursor.execute("CREATE TABLE IF NOT EXISTS "
        + dislikes_table + " ("
        + " user_id TEXT, "
        + " article_id INTEGER,"
        + " FOREIGN KEY(article_id)"
        + " REFERENCES articles (id));"
    )


# url to retrieve top stories ids
ts_url = "https://hacker-news.firebaseio.com/v0/topstories.json/"

# initialize articles table with top stories articles
def init_articles():
    # create request session to retrieve json data
    session = requests.Session()
    ids = session.get(ts_url)
    
    # parse json data into useable format, creating a list of 25 ids
    ids_list = ids.content
    ids_list = ids_list.decode()
    ids_list = ids_list[1:-1]
    ids_list = ids_list.split(",")
    ids_list = ids_list[:25]
    articles = []
    
    # iterate through each id and retrieve specific article json data, append to a list
    for id in ids_list:
        articles.append(session.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty").json())
    
    # capture upload date
    init_date = datetime.datetime.now()
    
    # if url key not available, expulse from list
    for node in articles:
        if "url" not in node:
            articles.remove(node)
    
    # shorten articles list to 15, originally saved 25 to practically guarantee enough articles with url keys are present
    articles = articles[:15]
    
    # for each node in json list insert into articles table in database
    for node in articles:
        cursor.execute("INSERT INTO " + articles_table + " VALUES (?, ?, ?, ?, ?)",
            (node['id'], node['title'], node['by'], node['url'], init_date))
    
    # commit changes and end request session
    connection.commit()
    session.close()

#
# could probably implement in a better fashion
#
# check if tables are present
articles_exists = cursor.execute(
    """SELECT name FROM sqlite_master WHERE type='table'
    AND name='articles';""").fetchall()

users_exists = cursor.execute(
    """SELECT name FROM sqlite_master WHERE type='table'
    AND name='users';""").fetchall()
    
likes_exists = cursor.execute(
    """SELECT name FROM sqlite_master WHERE type='table'
    AND name='likes';""").fetchall()
    
dislikes_exists = cursor.execute(
    """SELECT name FROM sqlite_master WHERE type='table'
    AND name='dislikes';""").fetchall()

# create table if not present
if articles_exists == []:
    create_articles()
    print("[init-db]: " + articles_table + " table has been created. Initalizing...")
    init_articles()
else:
    print("[init-db]: " + articles_table + " is present in database. Continuing...")

if users_exists == []:
    create_users()
    print("[init-db]: " + users_table + " table has been created. Continuing...")
else:
    print("[init-db]: " + users_table + " is present in database. Continuing...")
    
if likes_exists == []:
    create_likes()
    print("[init-db]: " + likes_table + " table has been created. Continuing...")
else:
    print("[init-db]: " + likes_table + " is present in database. Continuing...")
    
if dislikes_exists == []:
    create_dislikes()
    print("[init-db]: " + dislikes_table + " table has been created. Continuing...")
else:
    print("[init-db]: " + dislikes_table + " is present in database. Continuing...")

# commit changes and end database connection
connection.commit()
cursor.close()
connection.close()

# inform of program exit
print("[init-db]: Program exited.")
	
