class GeneralEvaluator:
    def __init__(self, user_list, job_list, job_total_score, _p_req, _p_prf):
        self._result = []
        self.user_list = user_list
        self.job_list = job_list
        self.job_total_score = job_total_score
        self._p_req = _p_req
        self._p_prf = _p_prf

    def evaluate(self):
        _score = 0
        self._result = []
        for field in self.job_list:
            _curr = self.find(field.field_data.title)
            self._result.append(_curr)
            print(field.field_data.title, _curr)
            if _curr:
                if field.is_required:
                    _score += self._p_req
                else:
                    _score += self._p_prf

        if _score > 0:
            _score = 100.0 * _score / self.job_total_score

        return self._result, _score, self._check()

    def find(self, field):
        return field in self.user_list

    def _check(self):
        idx = 0
        for field in self.job_list:
            if field.is_required and (not self._result[idx]):
                return False
            idx += 1
        return True

    @staticmethod
    def get_full_score(job_list, _p_req, _p_prf):
        _total = 0
        for field in job_list:
            if field.is_required:
                _total += _p_req
            else:
                _total += _p_prf
        return _total
