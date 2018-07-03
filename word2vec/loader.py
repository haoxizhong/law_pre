# coding:utf-8
import fasttext
import os


class Word2vec:
    def __init__(self, path):
        print("begin to load word embedding")

        self.model = fasttext.load_model(os.path.join(path, "model.bin"))

        print("load word embedding succeed")

    def load(self, word):
        return self.model[word]


if __name__ == "__main__":
    pass
