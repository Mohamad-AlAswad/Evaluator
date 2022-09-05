import datetime
import json
import time
import PyPDF2
import re
from utils.trie import Trie
import threading

jobs = {}
lazy_jobs = {}
lazy_jobs_delete = {}
users = {}
data = {}
all_type_cont = []
last_time = time.ctime()


class Container:
    def __init__(self, file_path):
        self.file_path = file_path
        self.trie = Trie()
        _temp = Repo.read_json_file(file_path)
        for item in _temp:
            self.__add(item)

    def remove(self, item):
        self.trie.remove(item)
        Repo.write_json_file(self.get_all(), self.file_path)

    def get(self, item, limit, exact):
        result = self.trie.query(item, exact, limit)
        if len(result) < limit:
            limit = len(result)
        return result[0:limit]

    def add(self, item):
        old_len = len(self.trie.all)
        self.trie.insert(item)
        if old_len != len(self.trie.all):
            Repo.write_json_file(self.get_all(), self.file_path)

    def __add(self, item):
        self.trie.insert(item)

    def get_all(self):
        return self.trie.all


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
