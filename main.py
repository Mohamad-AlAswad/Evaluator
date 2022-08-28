from job import Job
from user import User
from repository import Container, Repo
from flask import Flask, jsonify
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin

# Use a service account.
cred = credentials.Certificate('rms-f-ef128-b70f6b7abb1f.json')
app_firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
jobs = {}
users = {}
data = {}
all_type_cont = []
app = Flask('Evaluator')


@app.route('/api/recommended/<user_id>', methods=['GET'])
def get_recommended(user_id):
    return []


@app.route('/api/unavailable/<user_id>', methods=['GET'])
def get_unavailable(user_id):
    return []


@app.route('/api/<type_cont>/<word>', methods=['GET'])
def get_comp(type_cont, word):
    if type_cont not in data:
        return []
    else:
        return data.get(type_cont).get(word)


@app.route('/api/<type_cont>/<word>', methods=['POST'])
def post_comp(type_cont, word):
    if type_cont not in all_type_cont:
        data[type_cont] = Container(type_cont)
        all_type_cont.append(type_cont)
        Repo.write_json_file(all_type_cont, 'type_cont')

    data.get(type_cont).add(word)
    return jsonify('added successfully'), 201


def listen_jobs():
    def add_job(doc):
        jobs[doc.id] = Job.from_json(doc.id, doc.to_dict())

    def delete_job(doc_id):
        jobs.pop(doc_id)

    def on_snapshot_jobs(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                add_job(change.document)
            elif change.type.name == 'REMOVED':
                delete_job(change.document.id)

    db.collection('jobs').on_snapshot(on_snapshot_jobs)


def listen_users():
    def add_user(doc):
        users[doc.id] = User.from_json(doc.id, doc.to_dict())

    def delete_user(doc_id):
        users.pop(doc_id)

    def on_snapshot_user(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                add_user(change.document)
            elif change.type.name == 'REMOVED':
                delete_user(change.document.id)

    db.collection('user_info').on_snapshot(on_snapshot_user)


def read_keywords():
    _all_type_cont = Repo.read_json_file('type_cont')
    _data = {}
    for one_type in _all_type_cont:
        _data[one_type] = Container(one_type)

    return _all_type_cont, _data


if __name__ == '__main__':
    all_type_cont, data = read_keywords()
    # listen_jobs()
    # listen_user()
    app.run(host="192.168.98.250")
