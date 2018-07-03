import os
import json
import torch
import random
import numpy as np

from net.loader import accusation_dict, accusation_list, law_dict, law_list
from net.loader import get_num_classes


def check_crit(data):
    cnt = 0
    for x in data:
        if x in accusation_dict.keys():
            cnt += 1
        else:
            return False
    return cnt == 1


def check_law(data):
    arr = []
    for x, y, z in data:
        if x < 102 or x > 452:
            continue
        if not ((x, y) in law_dict.keys()):
            return False
        arr.append((x, y))

    arr = list(set(arr))
    arr.sort()

    cnt = 0
    for x in arr:
        if x in arr:
            cnt += 1  # return False
    return cnt == 1


def get_crit_id(data, config):
    for x in data:
        if x in accusation_dict.keys():
            return accusation_dict[x]


def get_law_id(data, config):
    for x in data:
        y = x
        if y in law_dict.keys():
            return law_dict[y]


def get_time_id(data, config):
    if data["death"]:
        return 301
    if data["forever"]:
        return 302
    return data["imprisonment"]


def analyze_crit(data, config):
    res = torch.from_numpy(np.zeros(get_num_classes("crit")))
    for x in data:
        if x in accusation_dict.keys():
            res[accusation_dict[x]] = 1
    return res


def analyze_law(data, config):
    res = torch.from_numpy(np.zeros(get_num_classes("law")))
    for x in data:
        y = x
        if y in law_dict.keys():
            res[law_dict[y]] = 1
    return res


def analyze_time(data, config):
    res = torch.from_numpy(np.zeros(get_num_classes("time")))

    opt = get_time_id(data, config)

    res[opt] = 1
    return res


word_dict = {}


def load(x, transformer):
    return transformer.load(x)
    
    try:
        return transformer[x].astype(dtype=np.float32)
    except Exception as e:
        return transformer['UNK'].astype(dtype=np.float32)


def get_word_vec(x, config, transformer):
    vec = load(x, transformer)
    return vec


cnt1 = 0
cnt2 = 0


def check_sentence(data, config):
    if len(data) > config.getint("data", "sentence_num"):
        return False
    for x in data:
        if len(x) > config.getint("data", "sentence_len"):
            return False
    return True


def generate_vector(data, config, transformer):
    vec = []
    len_vec = [0, 0]
    blank = torch.from_numpy(get_word_vec("BLANK", config, transformer))
    sentence_num = config.getint("data", "sentence_num")
    sentence_len = config.getint("data", "sentence_len")

    ly = min(len(data), sentence_num)
    for b in range(0, ly):
        x = data[b]
        temp_vec = []
        lx = min(len(x), sentence_len)
        len_vec.append(lx)
        len_vec[1] += 1
        for a in range(0, lx):
            y = x[a]
            len_vec[0] += 1
            z = get_word_vec(y, config, transformer)
            temp_vec.append(torch.from_numpy(z))
        while len(temp_vec) < sentence_len:
            temp_vec.append(blank)
        vec.append(torch.stack(temp_vec))

    temp_vec = []
    while len(temp_vec) < sentence_len:
        temp_vec.append(blank)

    while len(vec) < sentence_num:
        vec.append(torch.stack(temp_vec))
        len_vec.append(1)
    if len_vec[1] > sentence_num:
        gg
    for a in range(2, len(len_vec)):
        if len_vec[a] > sentence_len:
            print(data)
            gg
    if len(len_vec) != sentence_num + 2:
        gg

    return torch.stack(vec), torch.LongTensor(len_vec)


def parse(data, config, transformer):
    label_list = config.get("data", "type_of_label").replace(" ", "").split(",")
    label = []
    for x in label_list:
        if x == "crit":
            label.append(analyze_crit(data["meta"]["crit"], config))
        if x == "law":
            label.append(analyze_law(data["meta"]["law"], config))
        if x == "time":
            label.append(analyze_time(data["meta"]["time"], config))
    vector, len_vec = generate_vector(data["fact"], config, transformer)
    return vector, len_vec, torch.cat(label)


def check(data, config):
    # if not (check_sentence(data["fact"], config)):
    #    return False
    # if data["meta"]["time"]["imprisonment"] > 300:
    #    return False

    return True
