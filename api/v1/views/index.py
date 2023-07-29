#!/usr/bin/python3
"""Module for function that defines the handles for incoming requests"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """Handles status request"""
    return (jsonify({"status": "OK"}))


@app_views.route("/stats")
def stats():
    """Retrieves the number of each object by type"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User
               }
    stats = {}
    for key, value in classes.items():
        stats[key] = storage.count(value)
    return (jsonify(stats), 404)
