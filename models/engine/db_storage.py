#!/usr/bin/python3
""" class for sqlAlchemy """
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """ create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dic[key] = elem
        else:
            lista = [State, City, User, Place, Review, Amenity]
            for clase in lista:
                query = self.__session.query(clase)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem
        return (dic)

    def new(self, obj):
        """add a new element in the table
        """
        self.__session.add(obj)

    def save(self):
        """save changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete an element in the table
        """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """configuration
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """ calls remove()
        """
        self.__session.close()

    #def count(self, cls=None):
    #    """Counts the number of appended objects available in storage"""
    #    all_classes = classes.values()
    #    if not cls:
    #        count = 0
    #        for val in all_classes:
    #            count += len(models.storage.all(val).values())
    #    else:
    #        count = len(models.storage.all(cls).values())
    #    return (count)

    #def get(self, cls, id):
    #    """Searches for object and returns it based on given id"""
    #    if cls not in classes.values():
    #        return None
    #    all_classes = models.storage.all(cls)
    #    for v in all_classes.values():
    #        if (v.id == id):
    #            return v
    #    return None
    
    def get(self, cls, id):
        """A method to retrieve one object"""
        classes = self.all(cls)
        for key, value in classes.items():
            if key.split('.')[1] == id:
                return (value)
        return (None)

    def count(self, cls=None):
        """Counts the number of objects in storage"""
        if (cls):
            return (len(self.all(cls)))
        return (len(self.all()))
