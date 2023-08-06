import sqlite3

db = "news.db"

connection = sqlite3.connect(db)
cursor = connection.cursor()

#order table by datetime 
#cursor.execute("CREATE TABLE test2 AS SELECT * FROM articles ORDER BY date DESC;")

# return articles with no likes
#cursor.row_factory = lambda cursor, row: row[0]
limit = 3
#cursor.execute("CREATE TABLE test2 AS SELECT id FROM articles WHERE id NOT IN(SELECT DISTINCT article_id FROM likes) ORDER BY date ASC LIMIT 5;")
cursor.execute("DELETE FROM articles WHERE id IN (SELECT id FROM articles WHERE id NOT IN(SELECT DISTINCT article_id FROM likes) ORDER BY date ASC LIMIT 5);")
connection.commit()

cursor.close()
connection.close()
