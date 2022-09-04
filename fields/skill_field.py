class Skill:
    def __init__(self, title):
        self.title = title

    @staticmethod
    def from_json(_data):
        return Skill(_data['title'])
