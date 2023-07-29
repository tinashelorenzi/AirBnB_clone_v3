#!/usr/bin/python3
"""
Module for function that defines the handles for incoming requests to
different routes
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Handles status request by returning a JSON with 'status' value OK
    """
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    """Retrieves the number of each object by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)