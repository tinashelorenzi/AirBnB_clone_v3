#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/states")
def get_states():
    """Retrieves and returns the list of all State objects"""
    states = storage.all(State)
    response = []
    for key, value in states.items():
        response.append(value.to_dict())
    return (jsonify(response))

@app_views.route("/states/<state_id>")
def gets_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state:
        return (jsonify(state.to_dict()), 200)
    abort(404)

@app_views.route("states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        return ({}, 200)
    abort(404)

@app_views.route("states", methods=["POST"])
def post_state():
    # Working on this currently
    pass

