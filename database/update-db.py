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

# establish connection to database
connection = sqlite3.connect(db)
cursor = connection.cursor()

# url to fetch new top stories ids 
ts_url = "https://hacker-news.firebaseio.com/v0/topstories.json/"

# function that will truncate the articles table
def truncate_articles(amt):
    cursor.execute("DELETE FROM dislikes WHERE article_id IN (SELECT id FROM articles WHERE id NOT IN(SELECT DISTINCT article_id FROM likes) ORDER BY date ASC LIMIT ?);", (amt,))
    cursor.execute("DELETE FROM articles WHERE id IN (SELECT id FROM articles WHERE id NOT IN(SELECT DISTINCT article_id FROM likes) ORDER BY date ASC LIMIT ?);", (amt, ))
    connection.commit()

# function which will snag new articles
def snag_articles():
    # create list of potential article ids to parse
    session = requests.Session()
    ids = session.get(ts_url)
    ids_list = ids.content
    ids_list = ids_list.decode()
    ids_list = ids_list[1:-1]
    ids_list = ids_list.split(",")
    ids_list = ids_list[25:]
    
    # create list of currently stored ids
    cursor.execute("SELECT id FROM articles")
    cursor.row_factory = lambda cursor, row: row[0]
    stored = cursor.fetchall()
    
    i = 0
    size = len(stored)
    
    # add new ids to the stored list
    for id in ids_list:
        # only add new id if not present in stored ids
        if int(id) in stored:
            continue
        else:
            stored.append(int(id))
        # continuing adding ids until the size of the stored increases by 5
        if size < (size + 5):
            i+=1
        # if size of stored ids has increased by 5 end loop
        if i == 5:
            break
    
    # new ids will be the last 5 elements of stored list
    # these articles are expected to be added but will only be added if they have a valid URL
    expected = stored[-5:]
    articles = []
    
    # add the expected ids json data to articles
    for id in expected:
        articles.append(session.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty").json())
    
    # check if the json data has URL key if so append to list of valid articles
    valid = []
    for key in articles:
        if "url" in key:
            valid.append(key)
    
    # output to sysadmin whats being added
    print("****************** update-db ******************")
    print("[update-db]: Articles being added to the database.")
    print(json.dumps(valid, indent=4))
    print("***********************************************")
    
    # insert the valid article json data to articles
    init_date = datetime.datetime.now()
    
    for node in valid:
        cursor.execute("INSERT OR IGNORE INTO " + articles_table + " VALUES (?, ?, ?, ?, ?)",
            (node['id'], node['title'], node['by'], node['url'], init_date))
            
    connection.commit()
    session.close()
    
    truncate_articles(len(valid))

snag_articles()
cursor.close()
connection.close()
print("[update-db]: Program Exited.")
