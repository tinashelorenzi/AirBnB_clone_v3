#!/usr/bin/python3
"""Initialization for the flask application are done here"""
from flask import Flask, jsonify, abort
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(arg):
    """Removes the current Session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handles request to unhandled paths"""
    return (jsonify({ "error": "Not found" }), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
