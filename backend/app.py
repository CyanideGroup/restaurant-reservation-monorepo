import functools
import json
import os

import flask

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth

app = flask.Flask(__name__)
CREDENTIALS_FILENAME = 'api_gateway/app_credentials.txt'
f = open(CREDENTIALS_FILENAME)
GOOGLE_CLIENT_ID = f.readline().strip()
GOOGLE_CLIENT_SECRET = f.readline().strip()
app.secret_key = GOOGLE_CLIENT_SECRET

app.register_blueprint(google_auth.app)

@app.route('/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return 'You are not currently logged in.'

app.run()