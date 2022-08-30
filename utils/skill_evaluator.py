from utils.general_evaluator import GeneralEvaluator


class SkillEvaluator:
    _p_req = 1
    _p_prf = 2

    def __init__(self, user_skills, job_skills, job_total_score):
        self._result = []
        self.user_skills = user_skills
        self.job_skills = job_skills
        self.job_total_score = job_total_score

    def evaluate(self):
        return GeneralEvaluator(
            user_list=self.user_skills,
            job_list=self.job_skills,
            job_total_score=self.job_total_score,
            _p_prf=SkillEvaluator._p_prf,
            _p_req=SkillEvaluator._p_req
        ).evaluate()

    @staticmethod
    def get_full_score(job_list):
        return GeneralEvaluator.get_full_score(
            job_list=job_list,
            _p_req=SkillEvaluator._p_req,
            _p_prf=SkillEvaluator._p_prf
        )
