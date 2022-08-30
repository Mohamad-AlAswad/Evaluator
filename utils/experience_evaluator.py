from utils.general_evaluator import GeneralEvaluator


class ExperienceEvaluator:
    _p_req = 1
    _p_prf = 2

    def __init__(self, user_experiences, job_experiences, job_total_score):
        self._result = []
        self.user_experiences = user_experiences
        self.job_experiences = job_experiences
        self.job_total_score = job_total_score

    def evaluate(self):
        _score, _advance = 0, 0
        self._result = []
        for experience in self.job_experiences:
            user_exp_period = self.find(experience.field_data.title)
            _delta = user_exp_period - experience.field_data.period
            _curr = _delta >= 0
            self._result.append(_curr)
            if _curr:
                if experience.is_required:
                    _score += self._p_req
                    _advance += self._p_req * _delta
                else:
                    _score += self._p_prf
                    _advance += self._p_prf * _delta

        if _score > 0:
            _score = 100.0 * _score / self.job_total_score

        return self._result, _score, self._check(), _advance

    def find(self, title):
        for _experience in self.user_experiences:
            if _experience.title == title:
                return _experience.period
        return -1

    def _check(self):
        idx = 0
        for experience in self.job_experiences:
            if experience.is_required and (not self._result[idx]):
                return False
            idx += 1
        return True

    @staticmethod
    def get_full_score(job_list):
        return GeneralEvaluator.get_full_score(
            job_list=job_list,
            _p_req=ExperienceEvaluator._p_req,
            _p_prf=ExperienceEvaluator._p_prf
        )
