import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from sqlalchemy.orm import relationship
from datetime import date
from database_connector import db_connector, sql_alchemy_connector
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import datetime
import service
import sqlalchemy

EMAIL_ADDR = 'cyanide_service@wp.pl'
PASSWORD = 'password'

DB_ADDRESS = '172.17.0.1'
RABBITMQ_URL = '172.17.0.1'
PORT = 5435

class NotificationService(service.Service):
    def __init__(self, name='notification_service', use_mock_database=False):
        """
        TODO: CHANGE DATABASE STRUCTURE!!!!!! (RESERVATION TO TABLE NOT RESTAURANT)
        :param name:
        :param use_mock_database:
        """
        super().__init__(name, table_names=['reservations', 'restaurants', 'tables'],
                         callables={'reservations': self.reservation_confirmation}, url=RABBITMQ_URL)
        if use_mock_database:
            self.db_con = db_connector.DBConnectorMock()
        else:
            base = declarative_base()
            class Restaurant(base):
                __tablename__ = 'restaurants'
                __table_args__ = {'schema': 'notification_microservice'}
                _id = Column(Integer, primary_key=True)
                name = Column(String)
                address = Column(String)

            class Table(base):
                __tablename__ = 'tables'
                __table_args__ = {'schema': 'notification_microservice'}
                _id = Column(Integer, primary_key=True)
                restaurant_id = Column(Integer, ForeignKey(
                    'notification_microservice.restaurants._id'))
                restaurant = relationship('Restaurant')

            class Reservation(base):
                __tablename__ = 'reservations'
                __table_args__ = {"schema": "notification_microservice"}
                _id = Column(Integer, primary_key=True)
                restaurant_id = Column(Integer, ForeignKey(
                    'notification_microservice.restaurants._id'))
                email = Column(String)
                date = Column(Date)
                time = Column(String)
                guests = Column(Integer)

            self.db_con = sql_alchemy_connector.\
                SQLAlchemyConnector([Restaurant, Reservation, Table],
                                    url=DB_ADDRESS+':'+str(PORT), db_name='postgres',
                                    username='notification_service', password='password')
            base.metadata.create_all(self.db_con.db)
        self.register_task(self.notify, 'notify')

    def reservation_confirmation(self, data):
        if 'method' in data.keys() and data['method'].upper() == 'CREATE':
            table = self.db_con.select('tables', filter={'_id': data['table_id']})[0]
            restaurant = self.db_con.select('restaurants', filter={'_id': table['restaurant_id']})[0]
            self.send_email(data['email'], topic='CYANIDE reservation confirmation',
                            message=f'This is a confirmation of your reservation for restaurant {restaurant["name"]}.\n'
                                    f'Reservation details:\n'
                                    f'restaurant: {restaurant["name"]}\n'
                                    f'address: {restaurant["address"]}\n'
                                    f'date: {data["date"]}\n'
                                    f'time: {data["time"]}')

    def send_email(self, address, topic, message):
        print()
        print(topic)
        print(message)
        pass
        # CALL EMAIL SENDING PROCEDURE VIA CELERY

    def get_today(self):
        return date.today()

    def notify(self):
        """
        goes through all the reservation records that are due today and sends
        and email. An email should be sent by invoking a task to a worker pool
        :return:

        TODO:
            create a worker pool (celery seems to be a good option for that)
        """
        Reservation = self.db_con.table_data['reservations']
        Restaurant = self.db_con.table_data['restaurants']
        data = self.db_con.session.query(Reservation, Restaurant).\
            filter(Reservation.restaurant_id == Restaurant._id).\
            filter(Reservation.date == datetime.date.today())
        for row in data:
            self.send_email(row.email, f'Your reservation at {row.name}',
                            f'This is a reminder of your for '
                            f'location {row.address}, {row.time},'
                            f'a table for {row.guests}')


if __name__ == '__main__':

    # initiating the service
    service = NotificationService(use_mock_database=False)

    # dropping tables for reinitialisation
    # service.drop_table('reservations')
    # service.drop_table('tables')
    # service.drop_table('restaurants')

    # clearing all tables (firstly the reservation table not to violate
    # constrains) and filling the restaurants table with initial data.
    # Since notification service is not the owner of any tables, it
    # normally would not have permission to edit them, hence the `force` flag
    # service.clear_table('reservations', force=True)
    # service.clear_table('tables', force=True)
    # service.clear_table('restaurants', force=True)

    # running the service. If reservation service is run afterwards, all the
    # reservation data added via reservation service will be automatically added
    # to reservations table of this service
    print('dziala')
    service.run()
