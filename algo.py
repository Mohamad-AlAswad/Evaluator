from repository import *
from entities.job import Job
from entities.user import User
from utils.evaluator import *


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
    _job = Job.from_json(doc.id, doc.to_dict())
    _job.set_scores(
        score_edu=EduQualificationEvaluator.get_full_score(_job.lis_edu),
        score_exp=ExperienceEvaluator.get_full_score(_job.lis_exp),
        score_lang=LanguageEvaluator.get_full_score(_job.lis_lang),
        score_skill=SkillEvaluator.get_full_score(_job.lis_skill)
    )
    jobs[doc.id] = _job


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
