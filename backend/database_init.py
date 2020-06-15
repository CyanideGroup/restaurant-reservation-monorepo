import datetime


def get_init_data():
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
        {'email': email, 'table_id': table_id, 'date': datetime.date.today(), 'time': datetime.time(11)}
        for reserv_id, email, table_id in zip(reserv_ids, emails, table_ids)]

    return restaurants_data, tables_data, reservations_data