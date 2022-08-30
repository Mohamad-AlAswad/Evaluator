from utils.general_evaluator import GeneralEvaluator


class EduQualificationEvaluator:
    _p_req = 1
    _p_prf = 2

    def __init__(self, user_edu_qualification, job_edu_qualification, job_total_score):
        self._result = []
        self.user_edu_qualification = user_edu_qualification
        self.job_edu_qualification = job_edu_qualification
        self.job_total_score = job_total_score

    def evaluate(self):
        return GeneralEvaluator(
            user_list=[_edu.title for _edu in self.user_edu_qualification],
            job_list=self.job_edu_qualification,
            job_total_score=self.job_total_score,
            _p_prf=EduQualificationEvaluator._p_prf,
            _p_req=EduQualificationEvaluator._p_req
        ).evaluate()

    @staticmethod
    def get_full_score(job_list):
        return GeneralEvaluator.get_full_score(
            job_list=job_list,
            _p_req=EduQualificationEvaluator._p_req,
            _p_prf=EduQualificationEvaluator._p_prf
        )
