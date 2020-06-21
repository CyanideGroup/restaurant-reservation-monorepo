import pika
import callme
import datetime
from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS
import time
from database_init import get_init_data
from oauthlib.oauth2 import WebApplicationClient
import os
import requests
import json
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from user import User
import google_auth

app = Flask(__name__)
CORS(app)

CREDENTIALS_FILENAME = 'app_credentials.txt'
f = open(CREDENTIALS_FILENAME)
GOOGLE_CLIENT_ID = f.readline().strip()
GOOGLE_CLIENT_SECRET = f.readline().strip()
app.secret_key = GOOGLE_CLIENT_SECRET
login_manager = LoginManager()
login_manager.init_app(app)
notification_service = callme.Proxy(server_id='notification_service', amqp_host='localhost')
reservation_service = callme.Proxy(server_id='reservation_service', amqp_host='localhost')
search_service = callme.Proxy(server_id='search_service', amqp_host='localhost')
restaurant_service = callme.Proxy(server_id='restaurant_service', amqp_host='localhost')


GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

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

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add to database
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    response = [serialize_dict(rest) for rest in get_restaurants_by_owner(users_email)]
    # dict = {}
    # for values in response:
    #     dict[values['_id']] = values
    # return response
    return jsonify(response)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/manager/report")
def report():
    req = request
    user = current_user.id
    if user is None:
        return
    email = user.email
    restaurant_id = request.args.get('restaurant_id')
    restaurants = get_restaurants_by_owner(email)
    if restaurant_id not in [restaurant['_id'] for restaurant in restaurants]:
        return
    return get_report(restaurant_id)

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
    report = get_report(0)
    app.run()
