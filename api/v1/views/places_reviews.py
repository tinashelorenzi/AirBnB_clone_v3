#!/usr/bin/python3
""" Objects that handles all default RestFul API actions for places reviews"""
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
		strict_slashes=False)
def get_reviews(place_id):
	"""
	Retrieves te list of all places objects of a place specified by
	place_id
	"""
	list_reviews = []
	place = storage.get(Place, place_id)
	if not place:
		abort(404)
	for review in place.reviews:
		list_reviews.append(review.to_dict())

	return (jsonify(list_reviews))

@app_views.route('/reviews/<review_id>', methods=['GET'],
		strict_slashes=False)
def get_review(review_id):
	"""
	Retrieves a specific review based on th id passed
	"""
	review = storage.get(Review, review_id)
	if not review:
		abort(404)
	return (jsonify(review.to_dict()))

@app_views.route('/reviews/<review_id>', methods=['DELETE'],
		strict_slashes=False)
def delete_review(review_id):
	"""
	Deletes a review
	"""
	review = storage.get(Review, review_id)

	if not review:
		abort(404)
	storage.delete(review)
	storage.save()

	return (make_response(jsonify({}), 200))

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
		strict_slashes=False)
def post_review(place_id):
	"""
	Creates a Review
	"""
	place = storage.get(Place, place_id)
	user = None
	data = request.get_json()

	if not place:
		abort(404)
	if not data:
		abort(400, description="Not a JSON")
	if 'user_id' not in data:
		abort(404, description="Missing user_id")

	user = storage.get(User, data["user_id"])
	if not user:
		abort(404)
	instance = Review(**data)
	instance.user_id = user.id
	instance.place_id = place.id
	instance.save()
	return (make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_place(review_id):
	"""
	Updates a Review
	"""
	review = storage.get(Review, review_id)
	data = request.get_json()
	if not review:
		abort(404)

	if not data:
		abort(400, description="Not a JSON")

	ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

	for key, value in data.items():
		if key not in ignore:
			setattr(review, key, value)
	storage.save()
	return make_response(jsonify(review.to_dict()), 200)
