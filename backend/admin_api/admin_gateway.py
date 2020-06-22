# import pika
import callme
import datetime
from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS
import time
from database_init import get_init_data
# from oauthlib.oauth2 import WebApplicationClient
# import os
# import requests
import json
# from flask_login import (
#     LoginManager,
#     current_user,
#     login_required,
#     login_user,
#     logout_user,
# )
import flask

app = flask.Flask(__name__)
# CREDENTIALS_FILENAME = 'app_credentials.txt'
# f = open(CREDENTIALS_FILENAME)
# GOOGLE_CLIENT_ID = f.readline().strip()
# GOOGLE_CLIENT_SECRET = f.readline().strip()
# app.secret_key = GOOGLE_CLIENT_SECRET
CORS(app)

reservation_service = callme.Proxy(server_id='reservation_service', amqp_host='localhost')
restaurant_service = callme.Proxy(server_id='restaurant_service', amqp_host='localhost')

table_owners = {'restaurants': (restaurant_service, 'restaurant_service'),
                'tables': (restaurant_service, "restaurant_service"),
                'reservations': (reservation_service, 'reservation_service')}

def serialize_dict(dict):
    """
    Changes date to string.
    :param dict:
    :return:
    """
    result = {}
    for key, value in dict.items():
        key_serialized = str(key) if isinstance(key, datetime.date) or isinstance(key, datetime.time) else key
        value_serialized = str(value) if isinstance(value, datetime.date) or isinstance(value, datetime.time) else value
        result[key_serialized] = value_serialized
    return result

@app.route('/')
def index():
    return f'Available tables:{str(table_owners.keys())}'

@app.route('/<table_name>', methods=['GET', 'POST'])
def select(table_name):
    if request.method == 'GET':
        service_rpc = table_owners[table_name][0]
        result = service_rpc.use_server(table_owners[table_name][1]).select(table_name)
        result = [serialize_dict(row) for row in result]
        return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001)