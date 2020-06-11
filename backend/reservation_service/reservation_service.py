import os,sys,inspect

from sqlalchemy.orm import relationship

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from database_connector import sql_alchemy_connector
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import datetime
import database_connector.db_connector
import service
import sqlalchemy

class ReservationService(service.Service):
    def __init__(self, name='reservation_service', use_mock_database=False):
        super().__init__(name, table_names=['restaurants', 'reservations', 'tables'],
                         owned_tables=['reservations'])
        if use_mock_database:
            self.db_con = database_connector.db_connector.DBConnectorMock()
        else:
            # Defining the database
            base = declarative_base()
            class Restaurant(base):
                __tablename__ = 'restaurants'
                __table_args__ = {'schema': 'reservation_microservice'}
                _id = Column(Integer, primary_key=True)
                name = Column(String)
                opens = Column(sqlalchemy.types.Time)
                closes = Column(sqlalchemy.types.Time)
                timestep = Column(Integer)
                # address = Column(String)

            class Table(base):
                __tablename__ = 'tables'
                __table_args__ = {'schema': 'reservation_microservice'}
                _id = Column(Integer, primary_key=True)
                label = Column(String)
                restaurant_id = Column(Integer, ForeignKey(
                    'reservation_microservice.restaurants._id'))
                restaurant = relationship('Restaurant')
                smoking = Column(sqlalchemy.types.Boolean)
                outside = Column(sqlalchemy.types.Boolean)
                size = Column(Integer)

            class Reservation(base):
                __tablename__ = 'reservations'
                __table_args__ = {"schema": "reservation_microservice"}
                _id = Column(Integer, primary_key=True)
                table_id = Column(Integer, ForeignKey(
                    'reservation_microservice.tables._id'))
                table = relationship('Table')
                email = Column(String)
                date = Column(Date)
                time = Column(sqlalchemy.types.Time)
                guests = Column(Integer)

            # Assigning an SQLAlchemy database connector
            self.db_con = sql_alchemy_connector.SQLAlchemyConnector([Restaurant, Reservation, Table],
                                                                    url='localhost', db_name='postgres',
                                                                    username='reservation_service', password='password')

            # Creating the tables if they do not exist
            base.metadata.create_all(self.db_con.db)

        # defining the methods that this service can execute as an RPC server
        self.register_task(self.create_reservation, 'create_reservation')
        self.register_task(self.get_reservation_by_id, 'get_reservation_by_id')
        self.register_task(self.get_user_reservations, 'get_user_reservations')
        self.register_task(self.search_terms, 'search_terms')

    def search_terms(self, restaurant_id, date, filter=None):
        restaurant_info = self.db_con.select('restaurants', filter={'_id':restaurant_id})[0]
        opens = restaurant_info['opens']
        time_step = restaurant_info['timestep']
        closes = restaurant_info['closes']
        start_time = datetime.datetime.combine(date, opens)
        end_time = datetime.datetime.combine(date, closes)
        time = start_time
        times = []
        while time < end_time:
            times.append(time)
            time += datetime.timedelta(minutes=time_step)
        if filter is None:
            filter = {}
        filter['restaurant_id'] = restaurant_id
        tables = self.db_con.select('tables', filter=filter, as_dict=True)
        reservations = self.db_con.select('reservations', filter={'table_id': [t['_id'] for t in tables], 'date':date}, as_dict=True)
        data = {}
        reservation_time = datetime.timedelta(hours=3)
        for time in times:
            for table in tables:
                is_free = True
                for reservation in reservations:
                    if time not in data.keys():
                        data[time] = []
                    res_time = reservation['time']
                    res_datetime = datetime.datetime.combine(date, res_time)
                    if reservation['table_id'] == table['_id'] \
                        and time - reservation_time < res_datetime < time + reservation_time:
                        is_free = False
                        break
                if is_free:
                    data[time].append(table)
        return data

    def create_reservation(self, data):
        self.log('create reservation function called', type='RPC RECV')
        created, data = self.create_record('reservations', data)
        return created, data

    def get_user_reservations(self, user):
        return self.db_con.select('reservations', filter={'email': user})

    def get_reservation_by_id(self, id):
        return self.db_con.select('reservations', filter={'_id': id}, as_dict=False)


if __name__ == '__main__':

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
    tables_data = [{'_id': table_ids[i],'label': str(i), 'size': i % 3 + 2, 'restaurant_id': restaurant_ids[i % len(restaurant_names)],
                    'outside': i % 2, 'smoking': i % 2} for i in range(num_tables)]

    # generating initial reservations data
    user_names = ['tomek', 'robert', 'justyna', 'anton', 'khanh', 'pawel']
    emails = [f'{name}@gmail.com' for name in user_names]
    rest_ids = [i%len(restaurant_names) for i in range(len(user_names))]
    reserv_ids = [i for i in range(len(user_names))]
    reservations_data = [{'email': email, 'table_id': table_id, 'date': datetime.date.today(), 'time': datetime.time(11)}
                         for reserv_id, email, table_id in zip(reserv_ids, emails, table_ids)]


    # reservations_data = [
    #     {'email': email, 'restaurant_id': rest_id,
    #      'date': datetime.date.today(), 'time': 'breakfast'}
    #     for reserv_id, email, rest_id in zip(reserv_ids, emails, rest_ids)]

    # creating the service instance
    service = ReservationService(use_mock_database=False)

    # force-cleaning
    # service.clear_table('reservations')
    # service.clear_table('tables', force=True)
    # service.clear_table('restaurants', force=True)

    # Initiating tables
    # service.init_table('restaurants', restaurants_data, force=True)
    # service.init_table('tables', tables_data, force=True)
    # service.init_table('reservations', reservations_data)

    reservation_json = {'restaurant_id':rest_ids[0], 'email': 'new_email@gmail.com',
                        'date': datetime.date.today(), 'time': 'dinner'}
    # service.create_record('reservations', {'_id': 7, 'email': 'email@email.com', 'restaurant_id': 1,'date': datetime.date.today(), 'time': 'breakfast'})
    # service.create_reservation(reservation_json)
    # service.search_terms(restaurant_id=0, date=datetime.date.today())
    service.run()
