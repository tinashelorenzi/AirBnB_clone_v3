#!/usr/bin/python3
from flask import Blueprint
from models.state import State
"""Initializes the Blueprint"""


app_views = Blueprint("/api/v1", __name__)


from api.v1.views.index import *
