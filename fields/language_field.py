class Language:
    def __init__(self, title):
        self.title = title

    @staticmethod
    def from_json(_data):
        return Language(_data['title'])

    # def __eq__(self, other):
    #     if isinstance(other, Language):
    #         return self.title == other.title
    #     return False
    #
    # def __hash__(self):
    #     return hash([self.title])
