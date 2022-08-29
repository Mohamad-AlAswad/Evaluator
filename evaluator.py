from datetime import date
from job import Job
from repository import jobs


class EvaluatedUserJob:
    def __init__(self, job_id, score, edu_qualifications, experiences, languages, skills):
        self.job_id = job_id
        self.score = score
        self.edu_qualifications = edu_qualifications
        self.experiences = experiences
        self.languages = languages
        self.skills = skills

    def __ge__(self, other):
        return self.score >= other.score

    def export_json(self):
        return {
            'job_id': self.job_id,
            'score': self.score,
            'edu_qualifications': self.edu_qualifications,
            'experiences': self.experiences,
            'languages': self.languages,
            'skills': self.skills
        }


class Evaluator:
    _p_req_skill = 1
    _p_prf_skill = 2
    _p_req_lang = 1
    _p_prf_lang = 2
    _p_req_exp = 1
    _p_prf_exp = 2
    _p_req_edu = 1
    _p_prf_edu = 2

    def __init__(self, user):
        self.user = user
        self.last_time = date.today()
        self._build()

    def _build(self):
        self.recommended = []
        self.unavailable = []
        for _job in jobs.keys():
            evaluated, available = self._evaluate(jobs.get(_job), _job)
            if available:
                self.recommended.append(evaluated)
            else:
                self.unavailable.append(evaluated)

        # self.recommended = sorted(self.recommended)
        # self.unavailable = sorted(self.unavailable)

    def _evaluate(self, _job: Job, _job_id):
        def _calc(satis, descriptions, _prf, _req):
            score = 0
            idx = 0
            fail = False
            for desc in descriptions:
                if satis[idx]['satisfied']:
                    if desc.is_required:
                        score += _req
                    else:
                        score += _prf
                elif desc.is_required:
                    fail = True
                idx += 1
            return score, fail

        def _evaluate_skills():
            result = [{'satisfied', self.user.find_skill(skill)} for skill in _job.lis_skill]
            score, fail = _calc(result, _job.lis_skill, Evaluator._p_prf_skill, Evaluator._p_req_skill)
            return result, score, fail

        def _evaluate_languages():
            result = [{'satisfied', self.user.find_language(language)} for language in _job.lis_lang]
            score, fail = _calc(result, _job.lis_lang, Evaluator._p_prf_lang, Evaluator._p_req_lang)
            return result, score, fail

        def _evaluate_edu_qualifications():
            result = [{'satisfied', self.user.find_edu(edu)} for edu in _job.lis_edu]
            score, fail = _calc(result, _job.lis_edu, Evaluator._p_prf_edu, Evaluator._p_req_edu)
            return result, score, fail

        def _evaluate_experiences():
            result = [{'satisfied', self.user.find_exp(exp)} for exp in _job.lis_exp]
            score, fail = _calc(result, _job.lis_exp, Evaluator._p_prf_exp, Evaluator._p_req_exp)
            return result, score, fail

        def _start():
            score = 0
            available = True
            _result_experiences, _score, _available = _evaluate_experiences()
            score += _score
            available = available and _available
            _result_edu_qualifications, _score, _available = _evaluate_edu_qualifications()
            score += _score
            available = available and _available
            _result_languages, _score, _available = _evaluate_languages()
            score += _score
            available = available and _available
            _result_skills, _score, _available = _evaluate_skills()
            score += _score
            available = available and _available
            if score > 0:
                score = 100 * _job.score / score
            return EvaluatedUserJob(
                job_id=_job_id,
                score=score,
                languages=_result_languages,
                skills=_result_skills,
                experiences=_result_experiences,
                edu_qualifications=_result_edu_qualifications
            ), available

        return _start()

    @staticmethod
    def full_job_score(job: Job):
        def _calc(_prf, _req, list_desc):
            _score = 0
            for desc in list_desc:
                if desc.is_required:
                    _score += _req
                else:
                    _score += _prf
            return _score

        score = _calc(Evaluator._p_prf_edu, Evaluator._p_req_edu, job.lis_edu)
        score += _calc(Evaluator._p_prf_skill, Evaluator._p_req_skill, job.lis_skill)
        score += _calc(Evaluator._p_prf_exp, Evaluator._p_req_exp, job.lis_exp)
        score += _calc(Evaluator._p_prf_lang, Evaluator._p_req_lang, job.lis_lang)
        return score
