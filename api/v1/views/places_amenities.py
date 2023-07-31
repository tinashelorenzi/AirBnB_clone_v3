#!/usr/bin/python3
"""
This module contains implementations to handle all default RESTful API actions
"""
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response
from os import environ


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        return (jsonify(place.amenities))

    amenities = []
    for ids place.amenity_ids:
        amenities.append(storage.get(Amenity, ids))
    return (jsonify(amenities))


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object to a Place"""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return (make_response(jsonify({}), 200))


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """Link a Amenity to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place:
        abort(404)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return (make_response(jsonify(amenity.to_dict()), 200))
    
    if environ.get("HBNB_TYPE_STORAGE") == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.save()

    return (make_response(jsonify(amenity.to_dict()), 201))
