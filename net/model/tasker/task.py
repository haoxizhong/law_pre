import torch
import torch.nn as nn
import torch.nn.functional as F

from net.utils import generate_graph
from net.loader import get_num_classes


class FC(nn.Module):
    def __init__(self, config, task_id):
        super(FC, self).__init__()
        task_name = config.get("data", "type_of_label").replace(" ", "").split(",")
        self.fc1 = nn.Linear(config.getint("net", "fc1_feature"), get_num_classes(task_name[task_id]))
        self.fc2 = nn.Linear(config.getint("net", "fc1_feature"), config.getint("net", "fc1_feature"))
        self.relu = nn.ReLU()

    def forward(self, x, config):
        if config.getboolean("net", "more_fc"):
            return self.fc1(self.relu(self.fc2(x)))
        else:
            return self.fc1(x)


class Task(nn.Module):
    def __init__(self, config, usegpu, task_id):
        super(Task, self).__init__()
        pass

    def forward(self, x, config):
        pass
