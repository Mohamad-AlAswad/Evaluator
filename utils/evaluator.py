import time
from entities.job import Job
from repository import jobs, lazy_jobs, applications
from entities.evaluated_user_job import EvaluatedUserJob
from utils.skill_evaluator import SkillEvaluator
from utils.language_evaluator import LanguageEvaluator
from utils.experience_evaluator import ExperienceEvaluator
from utils.edu_qualification_evaluator import EduQualificationEvaluator


class Evaluator:
    def __init__(self, user):
        self.user = user
        self.last_time = None
        self.recommended = {}
        self.unavailable = {}
        self._recommended = []
        self._unavailable = []
        self.build()

    def build(self):
        def update(_job):
            evaluated, available = self._evaluate(jobs.get(_job), _job)
            if available:
                self._recommended.append(evaluated)
            else:
                self._unavailable.append(evaluated)

        keys = lazy_jobs.keys()
        if self.last_time is None:
            keys = jobs.keys()

        apps = applications.get(self.user.id)
        if apps is None:
            apps = []
        for _job in keys:
            if _job not in apps:
                update(_job)
            # if (self.last_time is None) or (self.last_time < jobs[_job].last_time):

        self.last_time = time.ctime()
        self.recommended = {_job.job_id: _job.export_json() for _job in sorted(self._recommended)}
        self.unavailable = {_job.job_id: _job.export_json() for _job in sorted(self._unavailable)}

    def _evaluate(self, _job: Job, _job_id):
        score = 0
        available = True

        _result_skills, _score, _available = SkillEvaluator(
            user_skills=self.user.skills,
            job_skills=_job.lis_skill,
            job_total_score=_job.score_skill
        ).evaluate()

        score += 0.25 * _score
        available = available and _available

        _result_languages, _score, _available = LanguageEvaluator(
            user_languages=self.user.languages,
            job_languages=_job.lis_lang,
            job_total_score=_job.score_lang
        ).evaluate()
        score += 0.25 * _score
        available = available and _available

        _result_edu_qualifications, _score, _available = EduQualificationEvaluator(
            user_edu_qualification=self.user.edu_qualifications,
            job_edu_qualification=_job.lis_edu,
            job_total_score=_job.score_edu
        ).evaluate()
        score += 0.25 * _score
        available = available and _available

        _result_experiences, _score, _available, advance_score = ExperienceEvaluator(
            user_experiences=self.user.experiences,
            job_experiences=_job.lis_exp,
            job_total_score=_job.score_exp
        ).evaluate()
        score += 0.25 * _score
        available = available and _available

        return EvaluatedUserJob(
            job_id=_job_id,
            score=score,
            advance_score=advance_score,
            languages=_result_languages,
            skills=_result_skills,
            experiences=_result_experiences,
            edu_qualifications=_result_edu_qualifications
        ), available
