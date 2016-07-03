import itertools as itt
import json

'''
    iterate over documents in a jsonl file
'''
class Jsonlo():

    def __init__(self, train_dir, test_dir):
        self.train = train_dir
        self.test = test_dir

    def train_iter(self):
        return = itt.tee((json.loads(line) for line in open(self.train)))

    def test_iter(self):
        return itt.tee((json.loads(line) for line in open(self.test)))


