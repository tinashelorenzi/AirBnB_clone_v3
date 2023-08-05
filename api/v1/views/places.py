#!/usr/bin/python3
""" Objects that handles all default RestFul API actions for places"""
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all places objects
    of a specific City
    """
    list_places = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for place in city.places:
        list_places.append(place.to_dict())

    return jsonify(list_places)


@app_views.route("/places/<place_id>/", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a specific place based on id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a place based on id provided
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(City, city_id)
    user = None
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    instance = Place(**data)
    instance.city_id = city.id
    instance.user_id = user.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """
    Updates a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    Searches returns a place depending on the JSON in the body of the request
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    places = []
    if (len(data) == 0 or all(len(v) == 0 for k, v in data.items())):
        # Case: All lists are empty
        # Retrieves all Place objects and returns them because
        # All lists are empty
        for k, v in storage.all(Place):
            places.append(v)
            return (jsonify(places))
    elif any(len(v) == 0 for k, v in data.items()):
        if (len(data["states"]) == 0 and len(data["cities"]) == 0):
            # Case: states and cities lists are empty, excluding amenities
            # Retrieves all Place objects, doesn't return until filtered with
            # amenities

            for k, v in storage.all(Place):
                places.append(v)
        elif (len(data["states"]) == 0 and len(data["cities"]) != 0):
            # Case: states list is empty but not cities
            # Retrieves all cities and then all places from those cities
            cities = []

            for city_id in data["cities"]:
                cities.append(storage.get(City, city_id))

            for city in cities:
                places += city.places

        elif (len(data["states"]) != 0 and len(data["cities"]) == 0):
            # Case: cities list is empty but not states
            # Retrieves all states and then the places in the cities in the
            # states
            states = []

            for state_id in data["states"]:
                states.append(storage.get(State, state_id))

            for state in states:
                for city in state.cities:
                    places += city.places
    else:
        # Case: cities and states list are not empty
        # Retrieves all states and the all cities and the all unique places in
        # both of the adding places in the State objects first
        states = []
        cities = []

        for state_id in data["states"]:
            states.append(storage.get(State, state_id))

        for city_id in data["cities"]:
            cities.append(storage.get(City, state_id))

        for state in states:
            for city in state.cities:
                place += city.places

        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if len(data["amenities"]) != 0:
        # Filters places results to include only places with the specified
        # amenity
        amenities = []
        for amenity_id in data["amenities"]:
            ameities.append(storage.get(Amenity, amenity_id))

        for place in places:
            for amenity in amenities:
                if amenity not in place.amenities:
                    places.remove(place)
                    continue
    return (jsonify(places))
