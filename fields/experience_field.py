class Experience:
    def __init__(self, title, period, start, end):
        self.title = title
        self.period = period
        self.start = start
        self.end = end

    # def similarity(self, other):
    #     if self.period < other.period:
    #         return 0
    #     else:
    #         return self.period - other.period

    @staticmethod
    def from_json_user(_data):
        period = None
        if _data['start'] is not None and _data['end'] is not None:
            period = (_data['end'].year - _data['start'].year) + (_data['end'].month - _data['start'].month) / 12
        return Experience(
            _data['title'],
            period,
            _data['start'],
            _data['end']
        )

    @staticmethod
    def from_json_job(_data):
        return Experience(
            _data['title'],
            _data['period'],
            None,
            None
        )

    # def __eq__(self, other):
    #     if isinstance(other, Experience):
    #         return self.title == other.title and self.period >= other.period
    #     return False
    #
    # def __hash__(self):
    #     return hash([self.period, self.title])
