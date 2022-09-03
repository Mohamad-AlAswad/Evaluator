from fields.fields import *
import time


class Job:
    def __init__(self, _id, summary, lis_edu, lis_skill, lis_lang, lis_exp):
        self.score_edu, self.score_skill, self.score_lang, self.score_exp = 0, 0, 0, 0
        self.id, self.summary = _id, summary
        self.lis_edu, self.lis_skill = lis_edu, lis_skill
        self.lis_lang, self.lis_exp = lis_lang, lis_exp
        self.last_time = time.ctime()

    def set_scores(self, score_edu, score_skill, score_lang, score_exp):
        self.score_edu = score_edu
        self.score_skill = score_skill
        self.score_lang = score_lang
        self.score_exp = score_exp

    @staticmethod
    def from_json(_id, data):
        return Job(
            _id,
            data['summary'],
            [JobField.from_json(d, EduQualification.from_json) for d in data['edu-qualifications']],
            [JobField.from_json(d, Skill.from_json) for d in data['skills']],
            [JobField.from_json(d, Language.from_json) for d in data['languages']],
            [JobField.from_json(d, Experience.from_json_job) for d in data['experiences']],
        )
