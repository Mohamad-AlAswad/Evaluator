class JobDescriptionField:
    def __init__(self, value, is_required):
        self.value, self.is_required = value, is_required

    @staticmethod
    def from_json(data):
        return JobDescriptionField(data['value'], data['isRequired'])


class Job:
    def __init__(self, id, summary, title, lis_edu, lis_skill, lis_lang, lis_exp):
        self.id, self.summary = id, summary
        self.title, self.lis_edu, self.lis_skill = title, lis_edu, lis_skill
        self.lis_lang, self.lis_exp = lis_lang, lis_exp

    @staticmethod
    def from_json(id, data):
        return Job(
            id,
            data['JobDescription']['summary'],
            data['JobDescription']['title'],
            [JobDescriptionField.from_json(d) for d in data['JobDescription']['eduQualification']],
            [JobDescriptionField.from_json(d) for d in data['JobDescription']['skills']],
            [JobDescriptionField.from_json(d) for d in data['JobDescription']['languages']],
            [JobDescriptionField.from_json(d) for d in data['JobDescription']['experience']],
        )
