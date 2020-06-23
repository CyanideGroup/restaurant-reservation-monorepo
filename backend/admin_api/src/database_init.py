import datetime
import json
from os.path import isfile


def get_init_data():

    has_files = isfile('restaurants.json') and isfile('tables.json') and isfile('reservations.json')

    if has_files:
        restaurants_data = json.load('restaurants.json')
        for row in restaurants_data:
            row['opens'] = datetime.datetime.strptime(row['opens'], '%H:%M:%S').time()
            row['closes'] = datetime.datetime.strptime(row['closes'], '%H:%M:%S').time()

        tables_data = json.load('tables.json')
        reservations_data = json.load('reservations.json')
        for row in reservations_data:
            row['time'] = datetime.datetime.strptime(row['time'], '%H:%M:%S').time()
            row['date'] = datetime.datetime.strptime(row['date'], '%Y.%m.%d').date()
        return restaurants_data, tables_data, reservations_data



    user_names = ['tomek', 'robert', 'justyna', 'anton', 'khanh', 'pawel']
    emails = [f'{name}@gmail.com' for name in user_names]

    restaurant_names = ['kfc', 'burgerking', 'subway', 'mcdonalds']
    addresses = [f'{name} street' for name in restaurant_names]
    restaurant_ids = [i for i in range(len(restaurant_names))]
    restaurants_data = [
        {'_id': id, 'name': name, 'address': address, 'opens': datetime.time(7), 'closes': datetime.time(23),
         'timestep': 30, 'owner': 'pawelzakieta97@gmail.com'} for id, name, address in
        zip(restaurant_ids, restaurant_names, addresses)]
    # return reservations_data

    # generating initial tables data
    num_tables = 32
    table_ids = [i for i in range(num_tables)]
    tables_data = [{'_id': table_ids[i], 'label': str(i), 'size': i % 3 + 2,
                    'restaurant_id': restaurant_ids[i % len(restaurant_names)],
                    'outside': i % 2, 'smoking': i % 2} for i in range(num_tables)]

    # generating initial reservations data
    reserv_ids = [i for i in range(len(user_names))]
    reservations_data = [
        {'email': email, 'table_id': table_id, 'date': datetime.date.today(), 'time': datetime.time(11), 'guests': 2}
        for reserv_id, email, table_id in zip(reserv_ids, emails, table_ids)]

    return restaurants_data, tables_data, reservations_data

if __name__ == '__main__':
    with open('restaurants.json') as json_file:
        data = json.load(json_file)
        data['opens'] = datetime.datetime.strptime(data['opens'], '%H:%M:%S').time()
        data['closes'] = datetime.datetime.strptime(data['closes'], '%H:%M:%S').time()
        print(data)
