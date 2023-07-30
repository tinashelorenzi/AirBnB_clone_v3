#!/usr/bin/python3
""" Objects that handles all default RestFul API actions for places"""
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
		strict_slashes=False)
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

	return (jsonify(list_places))


@app_views.route('/places/<place_id>/', methods=['GET'], strict_slashes=False)
def get_place(place_id):
	"""
	Retrieves a specific place based on id
	"""
	place = storage.get(Place, place_id)
	if not place:
		abort(404)
	return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
		strict_slashes=False)
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


@app_views.route('/cities/<city_id>/places', methods=['POST'],
		strict_slashes=False)
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
	if 'user_id' not in request.get_json():
		abort(400, "Missing user_id")
	if 'name' not in request.get_json():
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


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
	"""
	Updates a Place
	"""
	place = storage.get(Place, place_id)
	if not place:
		abort(404)

	if not request.get_json():
		abort(400, description="Not a JSON")

	ignore = ['id', 'state_id', 'created_at', 'updated_at']

	data = request.get_json()
	for key, value in data.items():
		if key not in ignore:
			setattr(place, key, value)
	storage.save()
	return make_response(jsonify(city.to_dict()), 200)
