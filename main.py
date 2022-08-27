import json
from job import Job
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('rms-f-ef128-b70f6b7abb1f.json')
app_firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
jobs = {}
skills = []

app = Flask('Evaluator')
api = Api(app)


class Skill(Resource):
    def get(self):
        word = str(request.args.get('word')).lower()
        result = []
        for skill in skills:
            if word in str(skill).lower():
                result.append(skill)
        return result


api.add_resource(Skill, '/skill')


def add_job(doc):
    jobs[doc.id] = Job.from_json(doc.id, doc.to_dict())


def delete_job(doc_id):
    jobs.pop(doc_id)


if __name__ == '__main__':
    with open('skills.json') as f:
        skills = json.load(f)


    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                add_job(change.document)
            elif change.type.name == 'REMOVED':
                delete_job(change.document.id)


    col_query = db.collection('jobs')
    # Watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

    app.run()
