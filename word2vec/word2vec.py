# coding:utf-8
import numpy as np
import os
import pickle


class Word2vec:
    word_num = 0
    vec_len = 0
    word2id = None
    vec = None

    def __init__(self, model_path):
        print("begin to load word embedding")
        f = open(os.path.join(model_path, "word2id.pkl"), "rb")
        (self.word_num, self.vec_len) = pickle.load(f)
        self.word2id = pickle.load(f)
        f.close()
        self.vec = np.load(os.path.join(model_path, "vec_nor.npy"))
        print("load word embedding succeed")

    def load(self, word):
        try:
            return self.vec[self.word2id[word]].astype(dtype=np.float32)
        except:
            return self.vec[self.word2id['UNK']].astype(dtype=np.float32)


if __name__ == "__main__":
    a = Word2vec()
    print(a.vec_len)
    print(a.load('，'))
