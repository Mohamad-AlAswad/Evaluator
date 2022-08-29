from user import EduQualification, Experience


class JobDescriptionField:
    def __init__(self, value, is_required):
        self.value, self.is_required = value, is_required

    @staticmethod
    def from_json(data, manip):
        return JobDescriptionField(manip(data['value']), data['isRequired'])


class Job:
    def __init__(self, _id, summary, title, lis_edu, lis_skill, lis_lang, lis_exp):
        self.id, self.summary = _id, summary
        self.title, self.lis_edu, self.lis_skill = title, lis_edu, lis_skill
        self.lis_lang, self.lis_exp = lis_lang, lis_exp
        self.score = 0

    def set_score(self, score):
        self.score = score

    @staticmethod
    def from_json(_id, data):
        return Job(
            _id,
            data['JobDescription']['summary'],
            data['JobDescription']['title'],
            [
                JobDescriptionField.from_json(d, lambda s: EduQualification.from_json(s)) for d in
                data['JobDescription']['eduQualification']
            ],
            [
                JobDescriptionField.from_json(d, lambda s: s)
                for d in data['JobDescription']['skills']
            ],
            [
                JobDescriptionField.from_json(d, lambda s: s)
                for d in data['JobDescription']['languages']
            ],
            [
                JobDescriptionField.from_json(d, lambda s: Experience.from_json_job(s))
                for d in data['JobDescription']['experience']
            ],
        )
