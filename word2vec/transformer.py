import os
import json

path = "/data/disk1/private/zhx/law/data/big"
out_path = "/data/disk1/private/zhx/law/data/big_new"

for file_name in os.listdir(path):
    f = open(os.path.join(path, file_name), "r")
    ouf = open(os.path.join(out_path, file_name), "w")

    for line in f:
        arr = []
        data = json.loads(line)
        for y in data["fact"]:
            arr.append([x for x in y if x != "\r" and x != "\n"])
        arr = [x for x in arr if x != []]

        print(json.dumps({"fact": arr, "meta": data["meta"]},ensure_ascii=False),file=ouf)

