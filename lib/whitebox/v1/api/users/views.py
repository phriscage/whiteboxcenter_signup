"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) +
        '/../../../../../lib')
from whitebox.v1.api.main import db_client
from whitebox.v1.api.util import crossdomain
from couchbase.exceptions import NotFoundError
## need to import all child models for now
from flask import Blueprint, jsonify, request, abort, make_response
import json
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

users = Blueprint('users', __name__)

