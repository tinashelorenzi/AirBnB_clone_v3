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
def stats():
    """Retrieves the number of each object by type"""
    classes = [Amenity, City, Place, Review, State, User]
    obj_names = ["amenities", "cities", "places", "reviews", "states", "users"]

    obj_nums = {}
    for c in range(len(classes)):
        obj_nums[obj_names[c]] = storage.count(classes[c])

    return jsonify(obj_nums)
