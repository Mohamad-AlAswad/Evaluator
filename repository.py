import json

jobs = {}
users = {}
data = {}
all_type_cont = []


class Container:
    def __init__(self, file_path):
        _temp = Repo.read_json_file(file_path)
        self.data = []
        for item in _temp:
            self._add(item)
        self.file_path = file_path

    def remove(self, item):
        if item in self.data:
            self.data.remove(item)
            Repo.write_json_file(self.get_all(), self.file_path)
            return True
        else:
            return False

    def get(self, item):
        result = []
        item = item.lower()
        for _item in self.data:
            if item in _item.lower():
                result.append(_item)
        return result

    def add(self, item):
        if self._add(item):
            self.data = sorted(self.data)
            Repo.write_json_file(self.get_all(), self.file_path)
            return True
        else:
            return False

    def get_all(self):
        return self.data

    def _add(self, item):
        if item not in self.data:
            self.data.append(item)
            return True
        else:
            return False


class Repo:
    @staticmethod
    def write_json_file(_data, file_path):
        with open(file_path + '.json', 'w') as f:
            f.write(json.dumps(_data, indent=2))

    @staticmethod
    def read_json_file(file_path):
        with open('data_json/' + file_path + '.json', 'r') as f:
            _data = json.load(f)
        return _data
