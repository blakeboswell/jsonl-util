import itertools as itt

'''
    iterate over documents in a jsonl file
'''
class Jsonlo(Object):

    def __init__(self, train_dir, test_dir):
        self.train = train_dir
        self.test = test_dir

    def line_iter():
        with open(self.train, 'r') as train, open(self.test, 'r') as test:
            train_x, train_y = itt.tee((json.loads(line) for line in train))
            test_x, test_y = itt.tee((json.loads(line) for line in test))
            return train_x, train_y, test_x, test_y

