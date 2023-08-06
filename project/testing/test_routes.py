import pytest
from flask import Flask, session
import json
import os
from wsgi import app

@pytest.fixture()
def cli():
    app.config.update({
	'TESTING': True,
	'SECRET_KEY': os.getenv('AUTH0_CLIENT_SECRET')
    })
    yield app

def test_news_logged_in(cli):
    with cli.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = {'userinfo': {'sub': 'normal'}}
        assert client.get('/news').status_code == 200

def test_news_no_login(cli):
    with cli.test_client() as client:
        assert client.get('/news').status_code == 200

def test_home_no_login(cli):
    with cli.test_client() as client:
        assert client.get('/').status_code == 200

def test_home_logged_in(cli):
    with cli.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = {'userinfo': {'sub': 'normal'}}
        assert client.get('/').status_code == 200

def test_callback_no_login(cli):
    with cli.test_client() as client:
        assert client.get('/callback').status_code == 302

def test_callback_logged_in(cli):
    with cli.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = {'userinfo': {'sub': 'normal'}}
        assert client.get('/callback').status_code == 302


def test_profile_no_login(cli):
    with cli.test_client() as client:
        assert client.get('/profile').status_code == 200

def test_profile_logged_in(cli):
    with cli.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = {'userinfo': {'sub': 'normal'}}
        assert client.get('/profile').status_code == 200


def test_admin_no_login(cli):
    with cli.test_client() as client:
        assert client.get('/admin').status_code == 200

def test_admin_logged_in(cli):
    with cli.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = {'userinfo': {'sub': 'normal'}}
        assert client.get('/admin').status_code == 200


#def test_delete_no_login(cli):
#    with cli.test_client() as client:
#        assert client.get('/delete-user/<1>').status_code == 200

def test_delete_logged_in(cli):
    with cli.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = {'userinfo': {'sub': 'normal'}}
        assert client.get('/delete-user/<1>').status_code == 302
