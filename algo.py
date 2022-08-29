from repository import *
from job import Job
from user import User
from evaluator import Evaluator


def get_recommended_jobs_for_user(user_id):
    return Evaluator(users.get(user_id)).recommended


def get_unavailable_jobs_for_user(user_id):
    return Evaluator(users.get(user_id)).unavailable


def get_complement(type_cont, word):
    if type_cont not in data:
        return []
    else:
        return data.get(type_cont).get(word)


def post_complement(type_cont, word):
    if type_cont not in all_type_cont:
        data[type_cont] = Container(type_cont)
        all_type_cont.append(type_cont)
        Repo.write_json_file(all_type_cont, 'type_cont')

    data.get(type_cont).add(word)


def add_job(doc):
    jobs[doc.id] = Job.from_json(doc.id, doc.to_dict())
    jobs[doc.id].set_score(Evaluator.full_job_score(jobs[doc.id]))


def delete_job(doc_id):
    jobs.pop(doc_id)


def add_user(doc):
    users[doc.id] = User.from_json(doc.id, doc.to_dict())


def delete_user(doc_id):
    users.pop(doc_id)


def read_keywords():
    all_type_cont = Repo.read_json_file('type_cont')
    for one_type in all_type_cont:
        data[one_type] = Container(one_type)
