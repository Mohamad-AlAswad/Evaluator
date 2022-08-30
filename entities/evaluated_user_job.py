class EvaluatedUserJob:
    def __init__(self, job_id, score, advance_score, edu_qualifications, experiences, languages, skills):
        self.job_id = job_id
        self.score = score
        self.advance_score = advance_score
        self.edu_qualifications = edu_qualifications
        self.experiences = experiences
        self.languages = languages
        self.skills = skills

    def __ge__(self, other):
        if self.score == other.score:
            return self.advance_score >= other.advance_score
        return self.score > other.score

    def export_json(self):
        return {
            'job_id': self.job_id,
            'score': self.score,
            'edu_qualifications': self.edu_qualifications,
            'experiences': self.experiences,
            'languages': self.languages,
            'skills': self.skills
        }
