from net.parser import ConfigParser
from net.model import CNNSeq
from net.file_reader import init_transformer
from net.data_formatter import generate_vector
from net.loader import init_loader

import torch
import thulac

from torch.autograd import Variable

configFilePath = "config/predictor.config"


class Predictor:
    def __init__(self):
        self.config = ConfigParser(configFilePath)

        self.batch_size = self.config.getint("data", "batch_size")

        self.task_name = self.config.get("data", "type_of_label").replace(" ", "").split(",")

        init_transformer(self.config)
        from net.file_reader import transformer
        init_loader(self.config)
        self.transformer = transformer

        self.cutter = thulac.thulac(model_path=self.config.get("data", "thulac"), seg_only=True)

        self.model = CNNSeq(self.config, True)
        self.model.load_state_dict(torch.load("model/model"))
        self.model = self.model.cuda()
        self.model.init_hidden(self.config, True)

        self.beta = self.config.getfloat("data", "beta")

    def cut(self, s):
        data = self.cutter.cut(s)
        result = []
        first = True
        for x, y in data:
            if x == " ":
                continue
            result.append(x)
        return result

    def cut_sentence(self, s):
        s = self.cut(s)
        res = [[]]
        for x in s:
            if x == "。":
                res.append([])
            else:
                res[-1].append(x)
        return res

    def generate_multi(self, arr):
        arr = torch.sigmoid(arr)
        arr = arr.numpy()
        print(arr)
        res = []

        for a in range(0, len(arr)):
            res.append([])
            for b in range(0, len(arr[0])):
                if arr[a][b] > 0:
                    res[a].append(b + 1)

        return res

    def generate_one(self, arr):
        arr = torch.max(arr, dim=1)
        arr = arr.numpy()
        print(arr)
        res = []
        for a in range(0, len(arr)):
            res.append(arr[a])

        return res

    def forward(self, content, len_vec):
        result = []
        for a in range(0, self.batch_size):
            result.append({})

        content = Variable(content).cuda()
        len_vec = Variable(len_vec).cuda()
        result = self.model.forward(content, len_vec, self.config)
        # print(result)

        res = []
        for a in range(0, self.batch_size):
            res.append({})
        arr = self.generate_multi(result[0])
        for a in range(0, len(arr)):
            res[a]["articles"] = arr[a]
        arr = self.generate_multi(result[1])
        for a in range(0, len(arr)):
            res[a]["accusation"] = arr[a]
        arr = self.generate_one(result[1])
        for a in range(0, len(arr)):
            res[a]["imprisonment"] = arr[a]

        return res

    def predict(self, content):
        real_size = len(content)

        while len(content) < self.batch_size:
            content.append(content[-1])

        len_vec = []

        for a in range(0, len(content)):
            content[a] = self.cut_sentence(content[a])
            content[a], length = generate_vector(content[a], self.config, self.transformer)
            len_vec.append(length)

        content = torch.stack(content)
        len_vec = torch.stack(len_vec)

        result = self.forward(content, len_vec)

        return result[:real_size]
