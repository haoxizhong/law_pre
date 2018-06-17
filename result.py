import argparse
import os
import json

parser = argparse.ArgumentParser()
parser.add_argument('--path', '-p')
args = parser.parse_args()

path = args.path
name = path.split("/")[-1]

key_list = ["mi_pre", "ma_pre", "mi_rec", "ma_rec", "mi_f1", "ma_f1", "cnt"]
task_list = ["crit", "law", "time"]

result = {}

for a in task_list:
    result[a] = {}
    for b in key_list:
        result[a][b] = 0

cnt = 0
try:
    while True:
        cnt += 1
        for task in task_list:
            f = open(os.path.join(path, "%d-%s" % (cnt, task)), "r")
            nowv = {}
            for a in range(0, 6):
                value = float(f.readline()[:-1].split("\t")[-1])
                nowv[key_list[a]] = value
            if nowv["mi_f1"] + nowv["ma_f1"] > result[task]["mi_f1"] + result[task]["ma_f1"]:
                for x in nowv.keys():
                    result[task][x] = nowv[x]
                result[task]["cnt"] = cnt
except Exception as e:
    print(e)

f = open("result/%s" % name, "w")
for x in ["law", "crit", "time"]:
    print(x, json.dumps(result[x]), file=f)
    print(x, json.dumps(result[x]))

f.close()
