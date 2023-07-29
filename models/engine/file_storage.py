#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import json
import shlex
import hashlib


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            dictionary = self.__objects
            for key in dictionary:
                partition = key.replace('.', ' ')
                partition = shlex.split(partition)
                if (partition[0] == cls.__name__):
                    dic[key] = self.__objects[key]
            return (dic)
        else:
            return self.__objects

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """serialize the file path to JSON file path
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ delete an existing element
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """ calls reload()
        """
        self.reload()

    def get(self, cls, id):
        """A method to retrieve one object"""
        classes = self.all(cls)
        for key, value in classes.items():
            if (key.split(".")[1] == id):
                return (value)
        return (None)

    def count(self, cls=None):
        """Counts the number of objects in storage"""
        if cls:
            obj_list = []
            obj_dict = FileStorage.__objects.values()
            for item in obj_dict:
                if type(item).__name__ == cls:
                    obj_list.append(item)
            return len(obj_list)
        else:
            obj_list = []
            for class_name in self.CNC:
                if class_name == 'BaseModel':
                    continue
                obj_class = FileStorage.__objects
                for item in obj_class:
                    obj_list.append(item)
            return len(obj_list)