class EvaluatedUserJob:
    def __init__(self, job_id, score, advance_score, edu_qualifications, experiences, languages, skills):
        self.job_id = job_id
        self.score = score
        self.advance_score = advance_score
        self.edu_qualifications = edu_qualifications
        self.experiences = experiences
        self.languages = languages
        self.skills = skills

    def __le__(self, other):
        if self.score == other.score:
            return self.advance_score >= other.advance_score
        return self.score > other.score

    def __lt__(self, other):
        if self.score == other.score:
            return self.advance_score >= other.advance_score
        return self.score > other.score

    def export_json(self):
        return {
            'score': self.score,
            'edu-qualifications': self.edu_qualifications,
            'experiences': self.experiences,
            'languages': self.languages,
            'skills': self.skills,
        }
