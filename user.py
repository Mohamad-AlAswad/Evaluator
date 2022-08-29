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

    def __eq__(self, other):
        if isinstance(other, EduQualification):
            return self.degree == other.degree and self.field == other.field
        return False

    def __hash__(self):
        return hash([self.degree, self.field])


class Experience:
    def __init__(self, title, period):
        self.title = title
        self.period = period

    def similarity(self, other):
        if self.period < other.period:
            return 0
        else:
            return self.period - other.period

    @staticmethod
    def from_json_user(data):
        return Experience(
            data['title'],
            data['end'] - data['start']
        )

    @staticmethod
    def from_json_job(data):
        return Experience(
            data['title'],
            data['period']
        )

    def __eq__(self, other):
        if isinstance(other, Experience):
            return self.title == other.title and self.period >= other.period
        return False

    def __hash__(self):
        return hash([self.period, self.title])


class User:
    def __init__(self, _id, edu_qualification, experiences, languages, skills, summary):
        self.edu_qualification = edu_qualification
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
        return edu in self.edu_qualification

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
