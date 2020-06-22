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
import google_auth

app = flask.Flask(__name__)
CREDENTIALS_FILENAME = 'app_credentials.txt'
f = open(CREDENTIALS_FILENAME)
GOOGLE_CLIENT_ID = f.readline().strip()
GOOGLE_CLIENT_SECRET = f.readline().strip()
app.secret_key = GOOGLE_CLIENT_SECRET
CORS(app)

app.register_blueprint(google_auth.app)
notification_service = callme.Proxy(server_id='notification_service', amqp_host='localhost')
reservation_service = callme.Proxy(server_id='reservation_service', amqp_host='localhost')
search_service = callme.Proxy(server_id='search_service', amqp_host='localhost')
restaurant_service = callme.Proxy(server_id='restaurant_service', amqp_host='localhost')


def create_restaurant(data):
    return restaurant_service.use_server('restaurant_service').create_restaurant(data)

def create_table(data):
    return restaurant_service.use_server('restaurant_service').create_table(data)

def delete_table(table_id):
    return restaurant_service.use_server('restaurant_service').delete_table(table_id)

def create_reservation(data):
    return reservation_service.use_server('reservation_service').create_reservation(data)

def get_restaurants(filter):
    return restaurant_service.use_server('restaurant_service').get_restaurants(filter)

def get_reservations_rest(restaurant_id):
    return restaurant_service.use_server('restaurant_service').get_reservations(restaurant_id)

def notify():
    notification_service.use_server('notification_service').notify()

def search_restaurants(date, time, guests, restaurant_name=None, location=None):
    return search_service.use_server('search_service').search(date, time, guests, restaurant_name, location)

def search_terms(restaurant_id, date, filters=None):
    return search_service.use_server('reservation_service').search_terms(restaurant_id, date, filters)

def get_restaurants_by_owner(owner):
    return restaurant_service.use_server('restaurant_service').get_restaurants({'owner': owner})

def get_report(restaurant_id):
    return restaurant_service.use_server('restaurant_service').get_report(restaurant_id)


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
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        # response = [serialize_dict(rest) for rest in get_restaurants_by_owner(user_info['email'])]
        # return jsonify(response)
        return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return 'You are not currently logged in.'

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        data = request.get_json()
        data['date'] = datetime.date(*data['date'].split('.'))
        data['time'] = datetime.time(*data['date'].split(':'))
        created, data = create_reservation(data)
        return f'Reservation ID: {data["id"]}'
    date = datetime.date(*[int(arg) for arg in request.args.get('date').split('.')])
    restaurant_id = request.args.get('restaurant_id')
    days = request.args.get('days')
    if days is None:
        days = 30
    result = search_terms(restaurant_id, date)

    dict = {}
    for key, value in result.items():
        dict[str(key)] = value
    return dict

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        date = datetime.date(*[int(arg) for arg in request.args.get('date').split('.')])
        time = datetime.time(*[int(arg) for arg in request.args.get('time').split(':')])
        name = request.args.get('name')
        address = request.args.get('address')
        guests = request.args.get('guests')
        available_restaurants = search_restaurants(date, time, guests, name, address)
        for key, values in available_restaurants.items():
            available_restaurants[key]['opens'] = str(available_restaurants[key]['opens'])
            available_restaurants[key]['closes'] = str(available_restaurants[key]['closes'])
        return available_restaurants
    return 'nic'


@app.route("/manager/report")
def report():
    if not google_auth.is_logged_in():
        return

    user_info = google_auth.get_user_info()
    restaurant_id = int(request.args.get('restaurant_id'))
    restaurants = get_restaurants_by_owner(user_info['email'])
    if restaurant_id not in [restaurant['_id'] for restaurant in restaurants]:
        return
    report = get_report(restaurant_id)
    report = serialize_dict(report)
    for key, value in report.items():
        report[key] = serialize_dict(value)
    return report

if __name__ == '__main__':
    test = True
    if test:
        restaurants_data, tables_data, reservations_data = get_init_data()
        # Populating data
        for row in restaurants_data:
            create_restaurant(row)
        time.sleep(0.5)
        for row in tables_data:
            create_table(row)
        time.sleep(0.5)
        for row in reservations_data:
            create_reservation(row)
    # report = get_report(0)
    app.run(port=5000)
