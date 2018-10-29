# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from models import UserData
from flask import Flask, jsonify, request
import flask_cors
from google.appengine.ext import ndb
import google.auth.transport.requests
import google.oauth2.id_token
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)

# [START gae_python_user_data]
def query_user_data(user_id):
    """Fetches all data associated with user_id.

    Notes are ordered them by date created, with most recent note added
    first.
    """
    ancestor_key = ndb.Key(UserData, user_id)
    query = UserData.query(ancestor=ancestor_key).order(-UserData.created)
    user_data = query.fetch()

    user_data_dict = None
    ndb_user_obj = None
    for datum in user_data:
        ndb_user_obj = datum
        user_data_dict = {
            'user_id':datum.user_id,
            'has_completed_form': datum.has_completed_form,
            'created':datum.created
        }
        break

    return ndb_user_obj, user_data_dict
# [END gae_python_query_user_data]


@app.route('/user/data', methods=['GET'])
def get_user_info():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401
    # [END gae_python_verify_token]
    data = query_user_data(claims['sub'])[1]
    return jsonify(data)


@app.route('/user/data/onboarding')
def create_entry():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401
    if not query_user_data(claims['sub'])[1]:
        data_entry = UserData(
            parent=ndb.Key(UserData, claims['sub']),
            has_completed_form=False)
        data_entry.user_id = claims['sub']
        data_entry.put()
    return 'OK', 200


@app.route('/user/data/formcompleted')
def has_completed_form():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401
    user_data = query_user_data(claims['sub'])[0]
    result = {"status":user_data.has_completed_form}
    return jsonify(result)


@app.route('/user/data/updateformcompletionstatus', methods=['POST', 'PUT'])
def update_form_status():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401
    # [START gae_python_create_entity]
    data =  request.get_json()
    query_result =query_user_data(claims['sub'])
    user_data = query_result[0]
    user_data.has_completed_form = data['completedform']
    user_data.put()
    query_result[1]["has_completed_form"] = data['completedform']
    return jsonify(query_result[1])


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

