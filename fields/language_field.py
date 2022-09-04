class Language:
    def __init__(self, title):
        self.title = title

    @staticmethod
    def from_json(_data):
        return Language(_data['title'])
