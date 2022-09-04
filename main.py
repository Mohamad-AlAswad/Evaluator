import os
from flask import Flask, jsonify, request, send_file
from firebase_admin import credentials
import firebase_admin
from firebase_admin import firestore
from algo import *

cred = credentials.Certificate('config/rms-f-ef128-b70f6b7abb1f.json')
app_firebase = firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask('JOP-APIs')


@app.route('/api/rate-job-app/<job_id>/<rating>', methods=['GET'])
def update_job_app_rat(job_id, rating):
    rating = float(rating)
    if 0 <= rating <= 5:
        job_app_doc = db.collection('jobs-applications').document(job_id).get().to_dict()
        job_seeker_id = job_app_doc['job-seeker-id']
        job_seeker_doc = db.collection('user-info').document(job_seeker_id).get().to_dict()
        old = job_app_doc['rating']
        old = float(old)
        delta = rating - old
        counter = float(job_seeker_doc['--rating-counter'])
        old_rating = float(job_seeker_doc['rating']) * counter + delta
        if old != 0:
            counter -= 1
        if rating != 0:
            counter += 1
        if counter > 0:
            new_rating = old_rating / counter
        else:
            new_rating = 0
        db.collection('jobs-applications').document(job_id).update({'rating': rating})
        db.collection('user-info').document(job_seeker_id).update({'rating': new_rating, '--rating-counter': counter})
        return 'ok', 201
    else:
        return 'invalid rating', 400


@app.route('/api/recommended/<user_id>', methods=['GET'])
def get_recommended(user_id):
    return get_recommended_jobs_for_user(user_id)


@app.route('/api/unavailable/<user_id>', methods=['GET'])
def get_unavailable(user_id):
    return get_unavailable_jobs_for_user(user_id)


@app.route('/api/extract-cv/<user_id>', methods=['POST'])
def upload_pdf(user_id):
    save_path = 'upload_folder\\cv\\' + user_id + '.pdf'
    pdf_file = request.files['file']
    print(pdf_file.name)
    pdf_file.save(save_path)
    new_info = get_merged_user_info_from_pdf(user_id)
    print(new_info)
    db.collection('user-info').document(user_id).update(new_info)
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


@app.route('/api/<type_cont>/', methods=['GET'])
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
    return 'see the console!', 200


if __name__ == '__main__':
    listen_jobs()
    listen_users()
    read_keywords()

    # app.run(host="192.168.98.250")
    # app.run(host="192.168.137.1")
    app.run(host="192.168.137.223")
    # app.run(host="192.168.12.120")
