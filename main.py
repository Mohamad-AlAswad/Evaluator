from flask import Flask, jsonify
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
from algo import *

# Use a service account.
cred = credentials.Certificate('config/rms-f-ef128-b70f6b7abb1f.json')
app_firebase = firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask('Evaluator')


@app.route('/api/recommended/<user_id>', methods=['GET'])
def get_recommended(user_id):
    return get_recommended_jobs_for_user(user_id)


@app.route('/api/unavailable/<user_id>', methods=['GET'])
def get_unavailable(user_id):
    return get_unavailable_jobs_for_user(user_id)


@app.route('/api/<type_cont>/<word>', methods=['GET'])
def get_comp(type_cont, word):
    return get_complement(type_cont, word)


@app.route('/api/<type_cont>', methods=['GET'])
def get_comp_all(type_cont):
    return get_complement(type_cont, word='')


@app.route('/api/<type_cont>/<word>', methods=['POST'])
def post_comp(type_cont, word):
    post_complement(type_cont, word)
    return jsonify('added successfully'), 201


def listen_jobs():
    def on_snapshot_jobs(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                add_job(change.document)
            elif change.type.name == 'REMOVED':
                delete_job(change.document.id)

    db.collection('jobs').on_snapshot(on_snapshot_jobs)


def listen_users():
    def on_snapshot_user(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                add_user(change.document)
            elif change.type.name == 'REMOVED':
                delete_user(change.document.id)
            elif change.type.name == 'MODIFIED':
                delete_user(change.document.id)
                add_user(change.document)

    db.collection('user-info').on_snapshot(on_snapshot_user)


@app.route('/')
def debug_route():
    # for user in users:
    #     print('user', user)
    #
    # for job in jobs:
    #     print('job', job)
    return 'see the console!', 200


if __name__ == '__main__':
    read_keywords()
    listen_jobs()
    listen_users()
    # app.run(host="192.168.98.250")
    app.run(host="192.168.137.223")
