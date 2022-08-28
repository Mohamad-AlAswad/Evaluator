from job import Job
from repository import Container, Repo
from flask import Flask, request, jsonify

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('rms-f-ef128-b70f6b7abb1f.json')
app_firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
jobs = {}
data = {}
all_type_cont = []
app = Flask('Evaluator')


@app.route('/api/<type_cont>/<word>', methods=['GET'])
def get(type_cont, word):
    if type_cont not in data:
        return []
    else:
        return data.get(type_cont).get(word)


@app.route('/api/<type_cont>/<word>', methods=['POST'])
def post(type_cont, word):
    if type_cont not in all_type_cont:
        data[type_cont] = Container(type_cont)
        all_type_cont.append(type_cont)
        Repo.write_json_file(all_type_cont, 'type_cont')

    data.get(type_cont).add(word)
    return jsonify('added successfully'), 201


def add_job(doc):
    jobs[doc.id] = Job.from_json(doc.id, doc.to_dict())


def delete_job(doc_id):
    jobs.pop(doc_id)


if __name__ == '__main__':
    all_type_cont = Repo.read_json_file('type_cont')
    for one_type in all_type_cont:
        data[one_type] = Container(one_type)


    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                add_job(change.document)
            elif change.type.name == 'REMOVED':
                delete_job(change.document.id)


    col_query = db.collection('jobs')
    # Watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

    app.run(host="192.168.137.223")
