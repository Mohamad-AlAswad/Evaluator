from utils.general_evaluator import GeneralEvaluator


class LanguageEvaluator:
    _p_req = 1
    _p_prf = 2

    def __init__(self, user_languages, job_languages, job_total_score):
        self._result = []
        self.user_languages = user_languages
        self.job_languages = job_languages
        self.job_total_score = job_total_score

    def evaluate(self):
        return GeneralEvaluator(
            user_list=self.user_languages,
            job_list=self.job_languages,
            job_total_score=self.job_total_score,
            _p_prf=LanguageEvaluator._p_prf,
            _p_req=LanguageEvaluator._p_req
        ).evaluate()

    @staticmethod
    def get_full_score(job_list):
        return GeneralEvaluator.get_full_score(
            job_list=job_list,
            _p_req=LanguageEvaluator._p_req,
            _p_prf=LanguageEvaluator._p_prf
        )
