import os

accusation_list = []
accusation_dict = {}
law_list = []
law_dict = {}


def init(config):
    min_frequency = config.getint("data", "min_frequency")
    data_path = os.path.join(config.get("data", "data_path"), config.get("data", "dataset"))
    f = open(os.path.join(data_path, "crit.txt"), "r")
    cnt1 = 0
    for line in f:
        data = line[:-1].split(" ")
        name = data[0]
        num = int(data[1])
        if num > min_frequency:
            cnt1 += num
            accusation_list.append(name)
            accusation_dict[name] = len(accusation_list) - 1

    cnt2 = 0
    f = open(os.path.join(data_path, "lawx.txt"), "r")
    for line in f:
        data = line[:-1].split(" ")
        name = int(data[0])
        num = int(data[1])
        if num > min_frequency:
            cnt2 += num
            law_list.append(name)
            law_dict[name] = len(law_list) - 1

    print(len(accusation_list), cnt1)
    print(len(law_list), cnt2)


def get_num_classes(s):
    if s == "crit":
        return len(accusation_list)
    if s == "law":
        return len(law_list)
    if s == "time":
        return 25 * 12 + 3
    gg


def get_name(s, num):
    if s == "crit":
        return accusation_list[num]
    if s == "law":
        return law_list[num]
    if s == "time":
        if num <= 300:
            return str(num)
        else:
            if num == 301:
                return "死刑"
            else:
                return "无期"

    gg
