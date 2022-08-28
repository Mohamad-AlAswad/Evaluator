class EduQualification:
    def __init__(self, degree, field):
        self.degree = degree
        self.field = field

    @staticmethod
    def from_json(data):
        return EduQualification(
            data['degree'],
            data['field'],
        )


class Experience:
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end

    @staticmethod
    def from_json(data):
        return Experience(
            data['title'],
            data['start'],
            data['end']
        )


class User:
    def __init__(self, id, edu_qualification, experiences, languages, skills, summary):
        self.edu_qualification = edu_qualification
        self.experiences = experiences
        self.languages = languages
        self.skills = skills
        self.summary = summary
        self.id = id

    @staticmethod
    def from_json(id, data):
        return User(
            id,
            [EduQualification.from_json(_data) for _data in data['edu-qualification']],
            [Experience.from_json(_data) for _data in data['experiences']],
            data['languages'],
            data['skills'],
            data['summary']
        )
