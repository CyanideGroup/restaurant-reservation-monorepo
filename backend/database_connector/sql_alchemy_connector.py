from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_connector.db_connector import DBConnector

class SQLAlchemyConnector(DBConnector):
    def __init__(self, metadata_classes, url="localhost", db_name='postgres',
                 username='reservation_service', password='password'):
        self.table_data = {}
        for table_class in metadata_classes:
            self.table_data[table_class.__tablename__]=table_class
        db_string = f"postgres://{username}:{password}@{url}/{db_name}"
        self.db = create_engine(db_string)
        Session = sessionmaker(self.db)
        self.session = Session()

    def select(self, table_name, filter=None, like_filter=None, return_attr=None, as_dict=True, order_by=None, desc=False):
        table_class = self.table_data[table_name]
        objects = self.session.query(table_class)
        if filter is not None:
            for key, value in filter.items():
                if key[-4:] == '_max':
                    attribute = getattr(table_class, key[0:-4])
                    objects = objects.filter(attribute <= value)
                elif key[-4:] == '_min':
                    attribute = getattr(table_class, key[0:-4])
                    objects = objects.filter(attribute >= value)
                else:
                    attribute = getattr(table_class, key)
                    if isinstance(value, list):
                        objects = objects.filter(attribute.in_(value))
                    else:
                        objects = objects.filter(attribute == value)
        if like_filter is not None:
            for key, value in like_filter.items():
                attribute = getattr(table_class, key)
                objects = objects.filter(attribute.like(f'%{value}%'))
        if order_by is not None:
            if not desc:
                objects = objects.order_by(getattr(table_class, order_by))
            else:
                objects = objects.order_by(getattr(table_class, order_by).desc())
        if as_dict:
            objects = [self.row2dict(obj) for obj in objects]
        return objects

    def custom_query(self, table_name, filter=None, like_filter=None, return_attr=None, as_dict=True):
        table_class = self.table_data[table_name]
        objects = self.session.query(table_class)
        if filter is not None:
            for key, value in filter.items():
                if key[-4:] == '_max':
                    attribute = getattr(table_class, key[0:-4])
                    objects = objects.filter(attribute <= value)
                elif key[-4:] == '_min':
                    attribute = getattr(table_class, key[0:-4])
                    objects = objects.filter(attribute <= value)
                else:
                    attribute = getattr(table_class, key)
                    if isinstance(value, list):
                        objects = objects.filter(attribute.in_(value))
                    else:
                        objects = objects.filter(attribute == value)
        if like_filter is not None:
            for key, value in like_filter.items():
                attribute = getattr(table_class, key)
                objects = objects.filter(attribute.like(value))
        if as_dict:
            objects = [self.row2dict(obj) for obj in objects]
        return objects

    def create(self, table_name, data, commit=True):
        """
        :param table_name:
        :param data:
        :param commit:
        :return: True and id of newly created record if succeeded, False if an
        error occured
        TODO:
            At the current state there are 2 possible reasons for failure:
                - object with the given id already exists in the database
                  (in that case we should overwrite the record)
                - Some of the foreign keys are not yet in the database
                  (in this case we should return information about what foreign
                  keys are lacking so that the service can call the owner of
                  incomplete table and ask for the missing record)

        """
        table_class = self.table_data[table_name]
        object = table_class()
        for key, value in data.items():
            setattr(object, key, value)
        self.session.add(object)
        if commit:
            self.session.commit()
            return True, self.row2dict(object)

    def clear(self, table_name, commit=True):
        """
        deletes all rows from table
        :param table_name:
        :return:
        """
        table_class = self.table_data[table_name]
        self.session.query(table_class).delete()
        if commit:
            self.session.commit()
        return True

    def drop(self, table_name, commit=True):
        table_class = self.table_data[table_name]
        table_class.__table__.drop(self.db)
        if commit:
            self.session.commit()
        return True

    def update(self, table_name, data):
        """
        TODO:
            update method
        :param table_name:
        :return:
        """

    @staticmethod
    def row2dict(obj):
        obj_class = type(obj)
        return {c.name: getattr(obj, c.name) for c in obj_class.__table__.columns}

if __name__ == '__main__':
    base = declarative_base()
    class Restaurant(base):
        __tablename__ = 'restaurants'
        __table_args__ = {'schema': 'reservation_microservice'}
        _id = Column(Integer, primary_key=True)
        name = Column(String)


    db = SQLAlchemyConnector(metadata_classes=[Restaurant])
    objects = db.select('restaurants', order_by='name', desc=True)
    for restaurant in objects:
        print(restaurant)
    pass