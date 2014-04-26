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
from couchbase.exceptions import NotFoundError, KeyExistsError
## need to import all child models for now
from flask import Blueprint, jsonify, request, abort, make_response
import json
import time
import logging

logger = logging.getLogger(__name__)

users = Blueprint('users', __name__)

#create routes
@users.route('/new', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['GET'], headers='Content-Type')
#@requires_api_key
def create():
    """create a user

    **Example request:**

    .. sourcecode:: http

       GET /users/new HTTP/1.1
       Accept: application/json
        data: { 'email_address': abc@abc.com }

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

    :statuscode 200: success
    :statuscode 400: bad data
    """
    if not request.json:
        message = "must be application json"
        logger.warn(message)
        return jsonify(message=message, success=False), 400
    if not 'email_address' in request.json:
        message = "email_address is missing."
        logger.warn(message)
        return jsonify(message=message, success=False), 400
    email_address = request.json['email_address']
    key = "user::%s" % email_address
    values = {'created_at': time.time(), 'email_address': email_address}
    try:
        data = db_client.add(key, values)
    except KeyExistsError as error:
        message = "'%s' already exists." % email_address
        logger.warn(message)
        return jsonify(error=409, message=message, success=False), 409
    message = "'%s' added successfully!" % email_address
    logger.debug(message)
    return jsonify(message=message, success=True), 200


@users.route('/<email_address>', methods=['GET', 'OPTIONS'])
@crossdomain(origin="*", methods=['GET'], headers='Content-Type')
#@requires_api_key
def get(email_address):
    """get a user

    **Example request:**

    .. sourcecode:: http

       GET /users/abc@abc.com HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

    :statuscode 200: success
    :statuscode 400: bad data
    """
    key = "user::%s" % email_address
    try:
        data = db_client.get(key)
    except NotFoundError as error:
        message = "'%s' does not exist." % email_address
        logger.warn(message)
        return jsonify(error=404, message=message, success=False), 404
    if not data:
        message = "Something still is broke."
        return jsonify(error=500, message=message, success=False), 500
    message = "'%s' successfully found!" % email_address
    logger.debug(message)
    return jsonify(message=message, data=data.value, success=True), 200

