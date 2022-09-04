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

    # def __eq__(self, other):
    #     if isinstance(other, EduQualification):
    #         return self.degree == other.degree and self.field == other.field
    #     return False
    #
    # def __hash__(self):
    #     return hash([self.degree, self.field])
