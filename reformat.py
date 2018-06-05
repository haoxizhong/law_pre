import os
import json
import thulac

from net.parser import ConfigParser
from net.data_formatter import check_sentence

path = "/data/disk1/private/zhonghaoxi/cail/data/small"

cnt = 0
acc_dic = {}
f = open(os.path.join(path, "accu.txt"), "r")
for line in f:
    acc_dic[line[:-1]] = cnt
    cnt += 1
f.close()

cnt = 0
law_dic = {}
f = open(os.path.join(path, "law.txt"), "r")
for line in f:
    law_dic[int(line[:-1])] = cnt
    cnt += 1
f.close()

ouf = []
for a in range(0, 20):
    ouf.append(open(os.path.join(path, str(a)), "w"))

config = ConfigParser("/home/zhx/law_pre/config/default_local.config")

cutter = thulac.thulac(model_path=config.get("data", "thulac"), seg_only=True, filt=False)


def cut(s):
    data = cutter.cut(s)
    result = []
    first = True
    for x, y in data:
        if x == " ":
            continue
        result.append(x)
    return result


def cut_sentence(s):
    s = cut(s)
    res = [[]]
    for x in s:
        if x == "。":
            res.append([])
        else:
            res[-1].append(x)
    return res

debug = open("debug.out","w")


def solve_file(file_name, lower_bound, upper_bound):
    cnt = 0

    inf = open(os.path.join(path, file_name), "r")

    for line in inf:
        cnt += 1
        if cnt % 5000 == 0:
            print(cnt)

        data = json.loads(line)
        fact = cut_sentence(data["fact"])

        result = {
            "fact": fact,
            "meta": {
                "law": [],
                "crit": [],
                "time": {
                    "death": data["meta"]["term_of_imprisonment"]["death_penalty"],
                    "forever": data["meta"]["term_of_imprisonment"]["life_imprisonment"],
                    "imprisonment": data["meta"]["term_of_imprisonment"]["imprisonment"]
                }
            }
        }

        for x in data["meta"]["accusation"]:
            result["meta"]["crit"].append(acc_dic[x.replace("[","").replace("]","")])

        for x in data["meta"]["relevant_articles"]:
            result["meta"]["law"].append(law_dic[x])

        print(json.dumps(result, ensure_ascii=False), file=ouf[cnt % (upper_bound - lower_bound + 1) + lower_bound])


solve_file("train.json", 0, 14)
solve_file("test.json", 15, 19)
