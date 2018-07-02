import os
import json

path = "/data/disk1/private/zhx/law/data/big"
out_path = "/data/dis1k/private/zhx/law/data/one/data"

ouf = open(out_path, "w")

for file_name in os.listdir(path):
    f = open(os.path.join(path, file_name), "r")

    for line in f:
        arr = []
        data = json.loads(line)
        for x in data["fact"]:
            arr.append(" ".join(x))
        result = " 。 ".join(arr)
        print(result, file=ouf)

        break
    break
