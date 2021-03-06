# coding=utf8
import os,sys,inspect

from sqlalchemy.orm import relationship
from datetime import date
from database_connector import db_connector, sql_alchemy_connector
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
import datetime
import service
from database_init import get_init_data
import time
from _collections import OrderedDict

DB_ADDRESS = '172.17.0.1'
RABBITMQ_URL = '172.17.0.1'
PORT = 5432

class RestaurantService(service.Service):
    def __init__(self, name='restaurant_service', use_mock_database=False):
        super().__init__(name, table_names=['reservations', 'restaurants', 'tables'],
                         owned_tables=['restaurants', 'tables'], url=RABBITMQ_URL)
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
                owner = Column(String)
                price = Column(Integer)
                img1 = Column(String)
                img2 = Column(String)
                img3 = Column(String)
                description = Column(String)


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
                                    url=DB_ADDRESS+':'+str(PORT), db_name='postgres',
                                    username='restaurant_service', password='password')
            base.metadata.create_all(self.db_con.db)
        self.register_task(self.get_restaurants, 'get_restaurants')
        self.register_task(self.create_table, 'create_table')
        self.register_task(self.delete_table, 'delete_table')
        self.register_task(self.create_restaurant, 'create_restaurant')
        self.register_task(self.get_reservations_by_restaurant_id, 'get_reservations')
        self.register_task(self.get_report, 'get_report')

    def create_restaurant(self, data):
        self.log('create restaurant function called', type='RPC RECV', channel=self.rpc_channel)
        created, data = self.create_record('restaurants', data)
        return created, data

    def create_table(self, data):
        self.log('create table function called', type='RPC RECV', channel=self.rpc_channel)
        created, data = self.create_record('tables', data)
        return created, data

    def delete_table(self, table_id):
        self.log('delete table function called', type='RPC RECV')
        deleted = self.delete_record('tables', table_id)
        return deleted

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

    def get_report(self, restaurant_id, date=None, days=30):
        restaurant_info = self.db_con.select('restaurants', filter={'_id': restaurant_id})[0]
        tables = self.db_con.select('tables', filter={'restaurant_id': restaurant_id}, as_dict=True)
        opens = restaurant_info['opens']
        closes = restaurant_info['closes']
        if date is None:
            date = datetime.date.today()
        day = date - datetime.timedelta(days=days)
        resolution = datetime.timedelta(hours=1)
        result = {}
        while day <= date:
            time = datetime.datetime.combine(day, opens)
            result[day] = OrderedDict()
            while time < datetime.datetime.combine(day, closes):
                result[day][time.time()] = 0
                time += resolution
            reservations = self.db_con.select('reservations',
                                              filter={'table_id': [t['_id'] for t in tables],
                                                      'date': day})
            for reservation in reservations:
                closest = None
                for hour in result[day].keys():
                    if hour <=reservation['time']:
                        closest = hour
                    else:
                        break
                result[day][closest] += reservation['guests']
            day += datetime.timedelta(days=1)
        return result


if __name__ == '__main__':
    # creating the service instance
    service = RestaurantService(use_mock_database=False)
    time.sleep(1)
    # dropping tables for reinitialisation
    # service.drop_table('reservations')
    # service.drop_table('tables')
    # service.drop_table('restaurants')

    # force-cleaning
    # service.clear_table('reservations', force=True)
    # service.clear_table('tables', force=True)
    # service.clear_table('restaurants', force=True)


    # Initiating tables
    restaurants_data, tables_data, reservations_data = get_init_data()
    # service.init_table('restaurants', restaurants_data)
    # service.init_table('tables', tables_data)
    # service.init_table('reservations', reservations_data, force=True)
    print('dziala')
    service.run()
