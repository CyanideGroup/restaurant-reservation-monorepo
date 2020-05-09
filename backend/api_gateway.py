import pika
import callme
import datetime
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello Cyanide'

@app.route('/reservation', methods=['GET', 'POST'])
def create_reservation():
    if request.method == 'POST':
        data = request.get_json()
        reservation_json = {'email': 'new_email@gmail.com', 'date': data['date'], 'time': data['time'], 'guests': 3, 'restaurant_id': data['restaurantId']}
        proxy = callme.Proxy(server_id='reservation_service', amqp_host='localhost',)
        created, id = proxy.use_server('reservation_service').create_reservation(reservation_json)
        return f'Reservation ID: {id}'
    return 'Make a reservation'


if __name__ == '__main__':
    app.run()


# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# # channel.exchange_declare(exchange='new_reservation', exchange_type='fanout')

# restaurant_json = {'method': 'create', 'name': 'restaurant123',
#                    'address': 'restaurant street 123'}

# # channel.basic_publish(exchange='restaurants', routing_key='', body=str(restaurant_json))

# # RPC test
# print(created)
# print(id)

# print("[x] new reservation")
# connection.close()