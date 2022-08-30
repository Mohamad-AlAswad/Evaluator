class JobField:
    def __init__(self, is_required, field_data):
        self.is_required = is_required
        self.field_data = field_data

    @staticmethod
    def from_json(_data, manipulation):
        return JobField(_data['is-required'], manipulation(_data))

    # def __eq__(self, other):
    #     if isinstance(other, JobField):
    #         return self.title == other.title
    #     return False
    #
    # def __hash__(self):
    #     return hash([self.title])
