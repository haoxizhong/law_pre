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
        self.model_list = []

        self.task_name = self.config.get("data", "type_of_label").replace(" ", "").split(",")

        for name in self.task_name:
            self.model_list[name] = CNNSeq(self.config, True)
            self.model_list[name].load_state_dict(torch.load("model/%s" % name))
            self.model_list[name] = self.model_list[name].cuda()
            self.model_list[name].eval()

        init_transformer(self.config)
        from net.file_reader import transformer
        self.transformer = transformer

        self.cutter = thulac.thulac(model_path=self.config.get("data", "thulac"), seg_only=True)

    def cut(self, sentence):
        result = []
        for s in sentence:
            s = self.cutter.cut(s)
            print(s)
            gg

    def forward(self, content, len_vec):
        result = []
        for a in range(0, self.batch_size):
            result.append({})

        content = Variable(content).cuda()
        len_vec = Variable(len_vec).cuda()
        for name in self.task_name:
            res = self.model_list[name].forward(content, len_vec)
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
            content[a] = self.cut(content[a])
            content[a], length = generate_vector(content[a], self.transformer, self.config)
            len_vec.append(length)

        content = torch.stack(content)
        len_vec = torch.stack(len_vec)

        result = self.forward(content, len_vec)

        return result[:real_size]
