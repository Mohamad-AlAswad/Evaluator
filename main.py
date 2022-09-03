from flask import Flask, jsonify, request
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


@app.route('/api/extract-cv/<user_id>', methods=['POST'])
def upload_pdf(user_id):
    save_path = 'C:\\Users\\creat\\PycharmProjects\\Evaluator\\upload_folder\\cv\\' + user_id
    pdf_file = request.files['file']
    pdf_file.save(save_path)
    update_user_info_from_pdf(user_id)
    return 'ok', 201


@app.route('/api/<type_cont>/<word>', methods=['GET'])
def get_comp(type_cont, word):
    exact, limit = False, 100
    if request.args.get('exact') and request.args.get('exact').lower() == 'true':
        exact = True
    if request.args.get('limit') is not None:
        try:
            if 1 <= int(request.args.get('limit')) <= 100:
                limit = int(request.args.get('limit'))
        except ValueError:
            limit = 100
    return get_complement(type_cont, word, limit, exact)


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
    update_user_info_from_pdf('KNvVSQq2xSUaxUNsEbHCu5VvHWv2')
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
    # app.run(host="192.168.137.1")
    app.run(host="192.168.137.223")
    # app.run(host="192.168.12.120")
