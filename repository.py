import json
import PyPDF2
import re

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

    def get(self, item, limit, exact):
        result = []
        item = item.lower()
        for _item in self.data:
            if exact and item == _item.lower():
                result.append(_item)
            if not exact and item in _item.lower():
                result.append(_item)
            if len(result) == limit:
                break
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
        with open('data_json/' + file_path + '.json', 'w') as f:
            f.write(json.dumps(_data, indent=2))

    @staticmethod
    def read_json_file(file_path):
        with open('data_json/' + file_path + '.json', 'r') as f:
            _data = json.load(f)
        return _data


class PdfCvReader:
    def __init__(self, file_path):
        self.words = PdfCvReader.__read_pdf_file(file_path)
        self.inp = PdfCvReader.__duplicate_words(self.words)

    def extract_type(self, key):
        result = []
        for word in self.inp:
            if data.get(key).get(word, 1, True):
                result.append(word)
        return result

    def extract_emails(self):
        return re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.words)

    def extract_phones(self):
        phones = re.findall(r"\+[-()\s\d]+?(?=\s*[+<])", self.words)
        return [re.sub("[^0-9]", "", phone) for phone in phones]

    @staticmethod
    def __read_pdf_file(file_path):
        result = ''
        with open('upload_folder/cv/' + file_path + '.pdf', 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            for page_number in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_number)
                page = page.extract_text()
                page = page.lower()
                page = page.split('\n')
                for line in page:
                    result = result + line
        return result

    @staticmethod
    def __duplicate_words(words):
        words = words.split(' ')
        result = []
        for i in range(len(words)):
            for j in range(7):
                temp = ''
                for k in range(j):
                    if i + k < len(words):
                        temp = temp + ' ' + words[i + k]
                result.append(temp.strip())
        return result
