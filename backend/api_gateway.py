import pika
import callme
import datetime
from flask import Flask, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)
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

def search(filter):
    return search_service.use_server('search_service').search(filter)


@app.route('/')
def index():
    return 'Hello Cyanide'

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        data = request.get_json()
        data['date'] = datetime.date(*data['date'].split('.'))
        data['time'] = datetime.time(*data['date'].split(':'))
        created, data = reservation_service.use_server('reservation_service').create_reservation(data)
        return f'Reservation ID: {data["id"]}'
    return 'Make a reservation'

@app.route('/search', methods=['GET', 'POST'])
def srch():
    if request.method == 'POST':
        data = request.get_json()
        reservation_json = {'email': 'new_email@gmail.com', 'date': data['date'], 'time': data['time'], 'guests': 3, 'restaurant_id': data['restaurantId']}
        created, data = reservation_service.use_server('reservation_service').create_reservation(reservation_json)
        return f'Reservation ID: {data["id"]}'
    return 'Make a reservation'

if __name__ == '__main__':
    test = True
    if test:
        # Generating initial restaurant table data
        restaurant_names = ['kfc', 'burgerking', 'subway', 'mcdonalds']
        addresses = [f'{name} street' for name in restaurant_names]
        restaurant_ids = [i for i in range(len(restaurant_names))]
        restaurants_data = [
            {'_id': id, 'name': name, 'address': address, 'opens': datetime.time(7), 'closes': datetime.time(23),
             'timestep': 30} for id, name, address in
            zip(restaurant_ids, restaurant_names, addresses)]

        # generating initial tables data
        num_tables = 32
        table_ids = [i for i in range(num_tables)]
        tables_data = [{'_id': table_ids[i], 'label': str(i), 'size': i % 3 + 2,
                        'restaurant_id': restaurant_ids[i % len(restaurant_names)],
                        'outside': i % 2, 'smoking': i % 2} for i in range(num_tables)]

        # generating initial reservations data
        user_names = ['tomek', 'robert', 'justyna', 'anton', 'khanh', 'pawel']
        emails = [f'{name}@gmail.com' for name in user_names]
        rest_ids = [i % len(restaurant_names) for i in range(len(user_names))]
        reserv_ids = [i for i in range(len(user_names))]
        reservations_data = [
            {'email': email, 'table_id': table_id, 'date': datetime.date.today(), 'time': datetime.time(11)}
            for reserv_id, email, table_id in zip(reserv_ids, emails, table_ids)]


        # Populating data
        for row in restaurants_data:
            create_restaurant(row)
        time.sleep(0.5)
        for row in tables_data:
            create_table(row)
        time.sleep(0.5)
        for row in reservations_data:
            create_reservation(row)
    
    # app.run()
