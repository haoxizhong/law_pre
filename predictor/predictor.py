from net.parser import ConfigParser
from net.model import CNNSeq
from net.file_reader import init_transformer
from net.data_formatter import generate_vector

import torch
import thulac

from torch.autograd import Variable

configFilePath = "config/predictor.config"


class Predictor:
    def __init__(self):
        self.config = ConfigParser(configFilePath)

        self.batch_size = self.config.getint("data", "batch_size")

        self.task_name = self.config.get("data", "type_of_label").replace(" ", "").split(",")

        self.model = CNNSeq(self.config, True)
        self.model.load_state_dict(torch.load("model/model"))

        init_transformer(self.config)
        from net.file_reader import transformer
        self.transformer = transformer

        self.cutter = thulac.thulac(model_path=self.config.get("data", "thulac"), seg_only=True)

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

    def forward(self, content, len_vec):
        result = []
        for a in range(0, self.batch_size):
            result.append({})

        content = Variable(content).cuda()
        len_vec = Variable(len_vec).cuda()
        result = self.model.forward(content, len_vec, self.config)

        gg
        for name in self.task_name:
            if name == "time":
                pass
            else:
                pass

        return result

    def predict(self, content):
        real_size = len(content)

        while len(content) < self.batch_size:
            content.append(content[-1])

        len_vec = []

        for a in range(0, len(content)):
            content[a] = self.cut_sentence(content[a])
            content[a], length = generate_vector(content[a], self.transformer, self.config)
            len_vec.append(length)

        content = torch.stack(content)
        len_vec = torch.stack(len_vec)

        result = self.forward(content, len_vec)

        return result[:real_size]
