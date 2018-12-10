import logging
from flask import Flask, jsonify, request
import flask_cors
import google.auth.transport.requests
import google.oauth2.id_token
import getRankedEmployers_old
import getRankedTeachers_old


app = Flask(__name__)
flask_cors.CORS(app)


@app.route('/matchmaker/classroomranking')
def classroom_matchmaker():
    employer_id = request.args.get("employer_id")
    ranker = getRankedTeachers_old.RankingTeachers(employer_id)
    list_of_ids = ranker.getRankedList()
    if list_of_ids is None :
        return jsonify({"result": "Missing keys in user data"})
    return jsonify({"result": list_of_ids})


@app.route('/matchmaker/employerranking')
def employer_matchmaker():
    teacher_id = request.args.get("teacher_id")
    ranker = getRankedEmployers_old.RankingEmployers(teacher_id)
    list_of_ids = ranker.getRankedList()
    if list_of_ids is None :
        return jsonify({"result": "Missing keys in user data"})
    return jsonify({"result": list_of_ids})


@app.route('/hello')
def hello():
    name = request.args.get("name")
    return "Hello, Your Name is {}!".format(name)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)