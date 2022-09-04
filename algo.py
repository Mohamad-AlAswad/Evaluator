from repository import *
from entities.job import Job
from entities.user import User
from utils.evaluator import *


def get_recommended_jobs_for_user(user_id):
    return Evaluator(users.get(user_id)).recommended


def get_unavailable_jobs_for_user(user_id):
    return Evaluator(users.get(user_id)).unavailable


def get_complement(type_cont, word, limit, exact):
    if type_cont not in data:
        return []
    else:
        return data.get(type_cont).get(word, limit, exact)


def post_complement(type_cont, word):
    if type_cont not in all_type_cont:
        data[type_cont] = Container(type_cont)
        all_type_cont.append(type_cont)
        Repo.write_json_file(all_type_cont, 'type_cont')

    data.get(type_cont).add(word)


def get_merged_user_info_from_pdf(user_id):
    def unique(duplicated_list):
        new_list = []
        for element in duplicated_list:
            if element not in new_list:
                new_list.append(element)
        return new_list

    def merge_dict(dic2, dic1):
        return dic1.update(dic2)

    def skills_user(skills):
        return {'skills': unique(skills + users[user_id].skills)}

    def languages_user(languages):
        return {'languages': languages + users[user_id].languages}

    def emails_user(emails):
        return {'emails': unique(emails + users[user_id].emails)}

    def phones_user(phones):
        return {'phones': unique(phones + users[user_id].phones)}

    def experiences_user(experiences):
        experiences = unique(experiences)
        old_experiences = [experience.title for experience in users[user_id].experiences]
        new_experiences = [
            {'title': experience.title, 'start': experience.start, 'end': experience.end}
            for experience in users[user_id].experiences
        ]
        for experience in experiences:
            if experience not in old_experiences:
                new_experiences.append({'title': experience, 'start': None, 'end': None})
        return {'experiences': new_experiences}

    content = PdfCvReader(user_id)
    new_info = skills_user(content.extract_type('skill'))
    merge_dict(languages_user(content.extract_type('language')), new_info)
    merge_dict(experiences_user(content.extract_type('job-title')), new_info)
    merge_dict(emails_user(content.extract_emails()), new_info)
    merge_dict(phones_user(content.extract_phones()), new_info)
    return new_info


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
        print(one_type)
        data[one_type] = Container(one_type)
