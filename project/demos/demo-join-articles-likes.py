import sqlite3

DB = "news.db"
ARTICLES_TABLE = "articles"
USERS_TABLE = "users"
LIKES_TABLE = "likes"

connection = sqlite3.connect(DB)
cursor = connection.cursor()

sub = "google-oauth2|112097886750082028328"

t = cursor.execute("CREATE TABLE test5 AS SELECT * FROM articles INNER JOIN likes ON likes.article_id=articles.id AND likes.user_id='" + sub + "';").fetchall()
connection.commit()
print("executed and committed")

cursor.close()
connection.close()
