import os,sys,inspect

from sqlalchemy.orm import relationship

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from datetime import date
from database_connector import db_connector, sql_alchemy_connector
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
import datetime
import service

class RestaurantService(service.Service):
    def __init__(self, name='restaurant_service', use_mock_database=False):
        super().__init__(name, table_names=['reservations', 'restaurants', 'tables'], owned_tables=['restaurants', 'tables'])
        if use_mock_database:
            self.db_con = db_connector.DBConnectorMock()
        else:
            base = declarative_base()
            class Restaurant(base):
                __tablename__ = 'restaurants'
                __table_args__ = {'schema': 'restaurant_microservice'}
                _id = Column(Integer, primary_key=True)
                name = Column(String)
                address = Column(String)
                country = Column(String)
                cuisine = Column(String)
                timestep = Column(Integer)
                opens = Column(sqlalchemy.types.Time)
                closes = Column(sqlalchemy.types.Time)
                rated = Column(Integer)

            class Table(base):
                __tablename__ = 'tables'
                __table_args__ = {'schema': 'restaurant_microservice'}
                _id = Column(Integer, primary_key=True)
                label = Column(String)
                restaurant_id = Column(Integer, ForeignKey(
                    'restaurant_microservice.restaurants._id'))
                restaurant = relationship('Restaurant')
                smoking = Column(sqlalchemy.types.Boolean)
                outside = Column(sqlalchemy.types.Boolean)
                size = Column(Integer)

            class Reservation(base):
                __tablename__ = 'reservations'
                __table_args__ = {"schema": "restaurant_microservice"}
                _id = Column(Integer, primary_key=True)
                table_id = Column(Integer, ForeignKey(
                    'restaurant_microservice.tables._id'))
                table = relationship('Table')
                date = Column(Date)
                time = Column(sqlalchemy.types.Time)
                guests = Column(Integer)


            self.db_con = sql_alchemy_connector.\
                SQLAlchemyConnector([Restaurant, Reservation, Table],
                                    url="localhost", db_name='postgres',
                                    username='restaurant_service', password='password')
            base.metadata.create_all(self.db_con.db)
        self.register_task(self.get_restaurants, 'get_restaurants')
        self.register_task(self.create_table, 'create_table')
        self.register_task(self.create_restaurant, 'create_restaurant')
        self.register_task(self.get_reservations_by_restaurant_id, 'get_reservations')

    def create_restaurant(self, data):
        self.log('create restaurant function called', type='RPC RECV')
        created, data = self.create_record('restaurants', data)
        return created, data

    def create_table(self, data):
        self.log('create restaurant function called', type='RPC RECV')
        created, data = self.create_record('tables', data)
        return created, data

    def get_restaurants(self, filter=None):
        self.log('get restaurant function called', type='RPC RECV')
        return self.db_con.select('restaurants', filter=filter)

    def get_reservations_by_restaurant_id(self, restaurant_id):
        reservations = self.db_con.select('reservations', filter={'restaurant_id': restaurant_id}, as_dict=False)
        data = []
        for reservation in reservations:
            row = self.db_con.row2dict(reservation)
            row['table'] = self.db_con.row2dict(reservation.table)
            data.append(row)
        return data


if __name__ == '__main__':
    # Generating initial restaurant table data
    restaurant_names = ['kfc', 'burgerking', 'subway', 'mcdonalds']
    addresses = [f'{name} street' for name in restaurant_names]
    restaurant_ids = [i for i in range(len(restaurant_names))]
    restaurants_data = [{'_id': id, 'name': name, 'address': address, 'opens':datetime.time(7), 'closes': datetime.time(23), 'timestep':30} for id, name, address in
                        zip(restaurant_ids, restaurant_names, addresses)]

    # generating initial tables data
    num_tables = 32
    table_ids = [i for i in range(num_tables)]
    tables_data = [{'_id': table_ids[i], 'label': str(i), 'size': i % 3 + 2,
                    'restaurant_id': restaurant_ids[i % len(restaurant_names)],
                    'outside': i % 2, 'smoking': i % 2} for i in range(num_tables)]

    # creating the service instance
    service = RestaurantService(use_mock_database=False)

    # force-cleaning
    service.clear_table('reservations', force=True)
    service.clear_table('tables', force=True)
    service.clear_table('restaurants', force=True)

    # Initiating tables
    # service.init_table('restaurants', restaurants_data)
    # service.init_table('tables', tables_data)
    # service.init_table('reservations', reservations_data, force=True)

    service.run()