"""
server.py
#
# description:
#
#
#
# maintained by:
# Carlos Pantoja-Malaga
# Matthew Kolnicki
#
"""
import json
import requests
import sqlite3

# flask and auth0 imports
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, flash

# get environment variables for auth0 integration
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# instantiate as flask application
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# handle OAuth registration for Auth0
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

def getUserId():
    """
    function which returns sub key from userinfo json node
    """
    # get session info json
    payload = json.dumps(session.get("user"))
    # load session info json as a string
    payload_s = json.loads(payload)
    # capture key sub from node userinfo
    sub = payload_s["userinfo"]["sub"]

    return sub

def getAdminVal():
    """
    function which returns administrator value for a user
    """
    # establish connection to the database
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    # query to execute, determine whether current user is an administrator
    sql_admin_query = "SELECT admin FROM users WHERE id=?;"
    cursor.execute(sql_admin_query, (getUserId(),))
    admin = cursor.fetchone()

    # handle admin values not 1
    if not admin:
        admin = 0
    else:
        admin = int(admin[0])

    # end connection to database
    cursor.close()
    connection.close()

    return admin

@app.route("/")
def home():
    """
    handle home route
    """
    # handle displaying admin panel if administrator
    admin = 0
    if session:
        admin = getAdminVal()

    return render_template(
        "home.html",
        session=session.get("user"),
        adminpanel=admin,
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    """
    handle callback route
    """
    # Auth0 callback handling
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    # establish connection to database
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    # need more data in case of saving a new user, can't use getUserId()
    payload = json.dumps(session.get("user"))
    payload_s = json.loads(payload)

    userinfo = payload_s["userinfo"]
    sub = userinfo["sub"]

    # query to execute, determine whether user is stored in users table in database
    sql_user_query = "SELECT id FROM users WHERE id=?;"

    cursor.execute(sql_user_query, (sub,))
    exists = cursor.fetchall()

    # if user is not found add to database
    if exists == []:
        # insert user into database, capture id, emaiil, name, and admin value at 0 for default
        sql_insert_query = "INSERT INTO users VALUES (?, ?, ?, ?);"
        cursor.execute(sql_insert_query,
            (sub, userinfo["email"], userinfo["name"], 0))
        connection.commit()

    # end connection to database
    cursor.close()
    connection.close()
    return redirect("/news")


@app.route("/login")
def login():
    """
    handle login route
    """
    # Auth0 login handling
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/logout")
def logout():
    """
    handle logout route
    """
    # Auth0 logout handling and clear session
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/news")
def news():
    """
    # Handle news route
    # NEED TO COMMENT
    """
    # establish connection to database
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row

    # select all articles utilize row factory to display properly
    sql_select_articles = "SELECT * FROM articles ORDER BY date DESC;"
    cursor.execute(sql_select_articles)
    articles = cursor.fetchall()

    # if in session handle displaying liked articles
    admin = 0
    if session:
        admin = getAdminVal()
        # handle capturing liked articles to display
        sql_select_liked = """SELECT title, url, author, id FROM articles INNER JOIN likes ON
			likes.article_id=articles.id AND likes.user_id=?;"""

        cursor.execute(sql_select_liked, (getUserId(),))

        liked_articles = cursor.fetchall()

        # handle capturing liked/disliked articles ids as a list
        # will use as a flag to enable button on frontend whether an article is
        #liked/disliked or not
        cursor.row_factory = lambda cursor, row: row[0]

        sql_flag_liked = "SELECT DISTINCT article_id FROM likes WHERE user_id=?;"
        sql_flag_disliked = "SELECT DISTINCT article_id FROM dislikes WHERE user_id=?;"

        cursor.execute(sql_flag_liked, (getUserId(),))
        liked_flag = cursor.fetchall()

        cursor.execute(sql_flag_disliked, (getUserId(),))
        disliked_flag = cursor.fetchall()

    else:
        liked_articles = []
        liked_flag = []
        disliked_flag = []

    # end connection to database
    cursor.close()
    connection.close()

    return render_template(
        "news.html",
        session=session.get("user"),
        articlestable=articles,
        adminpanel=admin,
        likedtable=liked_articles,
        likedflag=liked_flag,
        dislikedflag=disliked_flag,
        )


@app.route("/profile")
def profile():
    """
    handle profile route
    NEED TO COMMENT
    """
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row

    admin = 0

    if session:
        admin = getAdminVal()

        sql_select_liked = """SELECT title, url, author, id FROM articles INNER JOIN likes ON
				likes.article_id=articles.id AND likes.user_id=?;"""
        sql_select_disliked = """SELECT title, url, author, id FROM articles INNER JOIN dislikes ON
				dislikes.article_id=articles.id AND dislikes.user_id=?;"""

        cursor.execute(sql_select_liked, (getUserId(),))
        liked_articles = cursor.fetchall()

        cursor.execute(sql_select_disliked, (getUserId(),))
        disliked_articles = cursor.fetchall()

        cursor.row_factory = lambda cursor, row: row[0]

        sql_flag_liked = "SELECT DISTINCT article_id FROM likes WHERE user_id=?;"
        sql_flag_disliked = "SELECT DISTINCT article_id FROM dislikes WHERE user_id=?;"

        cursor.execute(sql_flag_liked, (getUserId(),))
        liked_flag = cursor.fetchall()

        cursor.execute(sql_flag_disliked, (getUserId(),))
        disliked_flag = cursor.fetchall()

    else:
        liked_articles = []
        disliked_articles = []
        liked_flag = []
        disliked_flag = []

    return render_template(
        "profile.html",
        session=session.get("user"),
        adminpanel=admin,
        likedtable=liked_articles,
        dislikedtable=disliked_articles,
        likedflag=liked_flag,
        dislikedflag=disliked_flag,
    )


@app.route("/admin")
def admin():
    """
    handle admin route
    NEED TO COMMENT
    """
    admin = 0
    if session:
        admin = getAdminVal()

    # establish connection to database
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row

    # capture articles within database
    sql_select_articles = "SELECT * FROM articles;"
    cursor.execute(sql_select_articles)
    articles = cursor.fetchall()

    # capture users within database
    sql_select_users = "SELECT * FROM users;"
    cursor.execute(sql_select_users)
    users = cursor.fetchall()

    sql_select_likes = """SELECT name, email, user_id, article_id FROM users INNER JOIN
                        likes ON users.id=likes.user_id;"""
    cursor.execute(sql_select_likes)
    likes = cursor.fetchall()

    sql_select_dislikes = """SELECT name, email, user_id, article_id FROM users INNER JOIN
                            dislikes ON users.id=dislikes.user_id;"""
    cursor.execute(sql_select_dislikes)
    dislikes = cursor.fetchall()

    # end connection to database
    cursor.close()
    connection.close()

    return render_template(
        "admin.html",
        session=session.get("user"),
        adminpanel=admin,
        articlestable=articles,
        usertable=users,
        likestable=likes,
        dislikestable=dislikes,
        )


@app.route("/like-article/<article_id>")
def like_article(article_id):
    """
    # handle like article route
    # liking article action handler
    #
    # TO-DO:
    # - if user likes a post and the post is disliked, remove the dislike
    #
    """

    # ensure user is logged in to handle liking articles
    if session:
        # establish connection to database
        connection = sqlite3.connect("news.db")
        cursor = connection.cursor()

        # query database to see if article being liked exists within database
        sql_article_exists = "SELECT id FROM articles WHERE id=?;"
        cursor.execute(sql_article_exists, (article_id,))
        article_exists = cursor.fetchall()

        # if the article does not exist inform user
        if article_exists == []:
            flash("This article UUID does not exist within the database.", category="error")
        else:
            # check if article is present in likes table
            sql_like = "SELECT * FROM likes WHERE article_id=? AND user_id=?;"
            cursor.execute(sql_like, (article_id, getUserId()))
            like_exists = cursor.fetchall()

            # if not present, add to likes table use user id and article id to identify like
            if like_exists == []:
                # query to insert into likes table
                sql_insert_like = "INSERT INTO likes VALUES (?,?);"
                cursor.execute(sql_insert_like, (getUserId(), article_id))

                # check if article is disliked
                sql_dislike = "SELECT * FROM dislikes WHERE article_id=? AND user_id=?;"
                cursor.execute(sql_dislike, (article_id, getUserId()))
                dislike_exists = cursor.fetchall()

                # if article is being liked, and is disliked, remove the dislike
                if dislike_exists:
                    sql_delete_dislike = "DELETE FROM dislikes WHERE article_id=? AND user_id=?;"
                    cursor.execute(sql_delete_dislike, (article_id, getUserId()))

                # commit change to database and inform user
                connection.commit()
                flash("You just liked article " + article_id + "!", category="success")
            # if present, remove like from likes table
            else:
                # query to delete from likes table
                sql_delete_like = "DELETE FROM likes WHERE article_id=? AND user_id=?;"
                cursor.execute(sql_delete_like, (article_id, getUserId()))

                # commit change and inform user
                connection.commit()
                flash("You just unliked article " + article_id + "!", category="error")

        cursor.close()
        connection.close()
    # if not logged in can not like post, inform user
    else:
        flash("You do not have sufficient permissions to perform this action.", category="error")
    return redirect("/news")


@app.route("/dislike-article/<article_id>")
def dislike_article(article_id):
    """
    handle dislike article route
    disliking article action handler

    TO-DO:
    - if user dislikes a post and the post is liked, remove the like
    """
    if session:
        connection = sqlite3.connect("news.db")
        cursor = connection.cursor()

        sql_article_exists = "SELECT id FROM articles WHERE id=?;"
        cursor.execute(sql_article_exists, (article_id,))
        article_exists = cursor.fetchall()

        if article_exists == []:
            flash("This article UUID does not exist within the database.", category="error")
        else:
            sql_dislike = "SELECT * FROM dislikes WHERE article_id=? AND user_id=?;"
            cursor.execute(sql_dislike, (article_id, getUserId()))
            dislike_exists = cursor.fetchall()

            if dislike_exists == []:
                sql_insert_dislike = "INSERT INTO dislikes VALUES (?, ?);"
                cursor.execute(sql_insert_dislike, (getUserId(), article_id))

                # check if article is liked
                sql_like = "SELECT * FROM likes WHERE article_id=? AND user_id=?;"
                cursor.execute(sql_like, (article_id, getUserId()))
                like_exists = cursor.fetchall()

                # if article is being disliked, and the article is liked, remove the like
                if like_exists:
                # query to delete from likes table
                    sql_delete_like = "DELETE FROM likes WHERE article_id=? AND user_id=?;"
                    cursor.execute(sql_delete_like, (article_id, getUserId()))

                connection.commit()
                flash("You disliked article " + article_id + "!", category="error")
            else:
                sql_delete_dislike = "DELETE FROM dislikes WHERE article_id=? AND user_id=?;"
                cursor.execute(sql_delete_dislike, (article_id, getUserId()))

                connection.commit()
                flash("You just removed your dislike for article " + article_id + "!",
                        category="error")
        cursor.close()
        connection.close()
    else:
        flash("You do not have sufficient permissions to perform this action.",
                category="error")
    return redirect("/news")

@app.route("/delete-user/<id>")
def delete_user(id):
    """
    # handle remove user route
    # removing user action handler
    """
    # check if administrator through admin value
    if getAdminVal() == 1:
        # establish connection to database
        connection = sqlite3.connect("news.db")
        cursor = connection.cursor()

        # utilize query to select id from users table, one unique value expected
        sql_user_exists = "SELECT id FROM users WHERE id=?;"
        cursor.execute(sql_user_exists, (id,))
        exists = cursor.fetchall()

        # if user id is not found inform user
        if exists == []:
            flash("This user UUID does not exist within the database.", category="error")

        # if user id is found within users table
        else:
            # utilize query to delete user id from users table
            sql_delete_user = "DELETE FROM users WHERE id=?;"
            cursor.execute(sql_delete_user, (id,))

            # query to delete user from likes table
            sql_delete_from_likes = "DELETE FROM likes WHERE user_id=?;"
            cursor.execute(sql_delete_from_likes, (id,))

            # query to delete user from dislikes table
            sql_delete_from_dislikes = "DELETE FROM dislikes WHERE user_id=?;"
            cursor.execute(sql_delete_from_dislikes, (id,))

            # commit deletion and inform administrator
            connection.commit()
            flash("User UUID: " + id + " has successfully been deleted from the database.",
                    category="success")

        # end connection to database
        cursor.close()
        connection.close()

    # if not administrator inform user of lack of permissions.
    else:
        flash("You do not have sufficient permissions to perform this action.", category="error")
    return redirect("/admin")


@app.route("/delete-article/<id>")
def delete_article(id):
    """
    handle delete user route
    removing user action handler

    """
    # check if administrator through admin value
    if getAdminVal() == 1:
        # establish database connection
        connection = sqlite3.connect("news.db")
        cursor = connection.cursor()

        # query to select id from articles table, one value expected
        sql_article_exists = "SELECT id FROM articles WHERE id=?;"
        cursor.execute(sql_article_exists, (id,))
        exists = cursor.fetchall()

        # if not present in database
        if exists == []:
            # inform user that article id is not present
            flash("This article UUID does not exist within the database.", category="error")

        # article is present in database
        else:
            # query to delete article from articles table
            sql_delete_article = "DELETE FROM articles WHERE id=?;"
            cursor.execute(sql_delete_article, (id,))

            # query to delete article from likes table
            sql_delete_from_likes = "DELETE FROM likes WHERE article_id=?;"
            cursor.execute(sql_delete_from_likes, (id,))

            # query to delete article from dislikes table
            sql_delete_from_dislikes = "DELETE FROM dislikes WHERE article_id=?;"
            cursor.execute(sql_delete_from_dislikes, (id,))

            # commit changes to article table and inform user
            connection.commit()
            flash("Article UUID: " + id + " has successfully been deleted from the database.",
                    category="success")

        cursor.close()
        connection.close()

    # if not an administrator inform user of lack of permission
    else:
        flash("You do not have sufficient permissions to perform this action.", category="error")
    return redirect("/admin")


@app.route("/delete-like/<user_id>/<article_id>")
def delete_like(user_id, article_id):
    """
    handle deleting like route
    deleting a like action handler
    NEED TO COMMENT
    """
    if getAdminVal() == 1:
        connection = sqlite3.connect("news.db")
        cursor = connection.cursor()

        sql_entry_exists = "SELECT user_id FROM likes WHERE user_id=? AND article_id=?;"
        cursor.execute(sql_entry_exists, (user_id, article_id))
        exists = cursor.fetchall()

        if exists == []:
            flash("The instance of this like does not exist within the database.", category="error")
        else:
            sql_delete_like = "DELETE FROM likes WHERE user_id=? AND article_id=?;"
            cursor.execute(sql_delete_like, (user_id, article_id))

            connection.commit()
            flash("Like by user UUID: " + user_id + " for article UUID: " + article_id +
                    " has successfully been deleted from the database.", category="success")
    else:
        flash("You do not have sufficient permissions to perform this action.", category="error")
    return redirect("/admin")


@app.route("/delete-dislike/<user_id>/<article_id>")
def delete_dislike(user_id, article_id):

    """
    handle deleting dislike route
    deleting a dislike action handler

    NEED TO COMMENT

    """
    if getAdminVal() == 1:
        connection = sqlite3.connect("news.db")
        cursor = connection.cursor()

        sql_entry_exists = "SELECT user_id FROM dislikes WHERE user_id=? AND article_id=?;"
        cursor.execute(sql_entry_exists, (user_id, article_id))
        exists = cursor.fetchall()

        if exists == []:
            flash("The instance of this dislike does not exist within the database.",
                    category="error")
        else:
            sql_delete_dislike = "DELETE FROM dislikes WHERE user_id=? AND article_id=?;"
            cursor.execute(sql_delete_dislike, (user_id, article_id))

            connection.commit()
            flash("Dislike by user UUID: " + user_id + " for article UUID: " + article_id +
                    " has successfully been deleted from the database.", category="success")
    else:
        flash("You do not have sufficient permissions to perform this action.", category="error")
    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
