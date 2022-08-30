from fields.fields import *


class User:
    def __init__(self, _id, edu_qualifications, experiences, languages, skills, summary):
        self.edu_qualifications = edu_qualifications
        self.experiences = experiences
        self.languages = languages
        self.skills = skills
        self.summary = summary
        self.id = _id

    def find_skill(self, skill):
        return skill in self.skills

    def find_language(self, language):
        return language in self.languages

    def find_edu(self, edu: EduQualification):
        return edu in self.edu_qualifications

    def find_exp(self, exp: Experience):
        return exp in self.experiences

    @staticmethod
    def from_json(_id, data):
        return User(
            _id,
            [EduQualification.from_json(_data) for _data in data['edu-qualifications']],
            [Experience.from_json_user(_data) for _data in data['experiences']],
            data['languages'],
            data['skills'],
            data['summary']
        )
