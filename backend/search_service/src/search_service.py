import os,sys,inspect

from sqlalchemy.orm import relationship

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from datetime import date
from database_connector import db_connector, sql_alchemy_connector
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
import datetime
import service

DB_ADDRESS = '172.17.0.1'
RABBITMQ_URL = '172.17.0.1'
# DB_ADDRESS = 'localhost'
# RABBITMQ_URL = 'localhost'
PORT = 5434

class SearchService(service.Service):
    def __init__(self, name='search_service', use_mock_database=False):
        super().__init__(name, table_names=['reservations', 'restaurants', 'tables'], url=RABBITMQ_URL)
        if use_mock_database:
            self.db_con = db_connector.DBConnectorMock()
        else:
            base = declarative_base()
            class Restaurant(base):
                __tablename__ = 'restaurants'
                __table_args__ = {'schema': 'search_microservice'}
                _id = Column(Integer, primary_key=True)
                name = Column(String)
                address = Column(String)
                country = Column(String)
                cuisine = Column(String)
                # timestep = Column(Integer)
                opens = Column(sqlalchemy.types.Time)
                closes = Column(sqlalchemy.types.Time)
                rated = Column(Integer)
                price = Column(Integer)
                img1 = Column(String)
                description = Column(String)

            class Table(base):
                __tablename__ = 'tables'
                __table_args__ = {'schema': 'search_microservice'}
                _id = Column(Integer, primary_key=True)
                restaurant_id = Column(Integer, ForeignKey(
                    'search_microservice.restaurants._id'))
                restaurant = relationship('Restaurant')
                # smoking = Column(sqlalchemy.types.Boolean)
                # outside = Column(sqlalchemy.types.Boolean)
                size = Column(Integer)

            class Reservation(base):
                __tablename__ = 'reservations'
                __table_args__ = {"schema": "search_microservice"}
                _id = Column(Integer, primary_key=True)
                table_id = Column(Integer, ForeignKey(
                    'search_microservice.tables._id'))
                table = relationship('Table')
                date = Column(Date)
                time = Column(sqlalchemy.types.Time)


            self.db_con = sql_alchemy_connector.\
                SQLAlchemyConnector([Restaurant, Reservation, Table],
                                    url=DB_ADDRESS+':'+str(PORT), db_name='postgres',
                                    username='search_service', password='password')
            base.metadata.create_all(self.db_con.db)
        self.register_task(self.search, 'search')


    def search(self, date, time, guests, restaurant_name=None, location=None):
        like_filter = {}
        if restaurant_name is not None:
            like_filter['name'] = restaurant_name
        if location is not None:
            like_filter['address'] = location
        restaurant_filter = {'opens_max':time, 'closes_min':time}
        res_duration = datetime.timedelta(hours=3)
        srch_datetime = datetime.datetime.combine(date, time)
        restaurants = self.db_con.select('restaurants', like_filter=like_filter, filter=restaurant_filter)
        tables = self.db_con.select('tables', filter={'restaurant_id': [r['_id'] for r in restaurants], 'size_min': guests})
        reservations = self.db_con.select('reservations', filter={'table_id': [t['_id'] for t in tables], 'date': date})
        free_restaurants = {}

        for table in tables:
            if table['restaurant_id'] in free_restaurants.keys():
                continue
            table_reservations = filter(lambda res:res['table_id']==table['_id'], reservations)
            occupied = False
            for res in table_reservations:
                res_time = datetime.datetime.combine(res['date'], res['time'])
                if res_time<srch_datetime+res_duration and res_time>srch_datetime-res_duration:
                    occupied = True
                    break
            if not occupied:
                free_restaurants[table['restaurant_id']] = list(filter(lambda x: x['_id'] == table['restaurant_id'], restaurants))[0]
        return free_restaurants

if __name__ == '__main__':
    # creating the service instance
    service = SearchService(use_mock_database=False)

    # dropping tables for reinitialisation
    # service.drop_table('reservations')
    # service.drop_table('tables')
    # service.drop_table('restaurants')

    # force-cleaning
    # service.clear_table('reservations', force=True)
    # service.clear_table('tables', force=True)
    # service.clear_table('restaurants', force=True)

    # Initiating tables
    # service.init_table('restaurants', restaurants_data, force=True)
    # service.init_table('tables', tables_data, force=True)
    # service.init_table('reservations', reservations_data, force=True)

    # service.search(date=datetime.date.today(), guests=1, time=datetime.time(6), restaurant_name='mcd')
    print('dziala')
    service.run()
