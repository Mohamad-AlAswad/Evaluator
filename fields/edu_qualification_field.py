class EduQualification:
    def __init__(self, degree, field):
        self.title = degree + ' $ ' + field

    @staticmethod
    def from_json(_data):
        if _data is None:
            return None
        return EduQualification(
            _data['degree'],
            _data['field'],
        )
