import os
import json

path = "/data/disk1/private/zhx/law/data/big"
out_path = "/data/disk1/private/zhx/law/data/one/data"

ouf = open(out_path, "w")

for file_name in range(0, 20):
    f = open(os.path.join(path, str(file_name)), "r")
    print(file_name)

    for line in f:
        arr = []
        data = json.loads(line)
        for y in data["fact"]:
            arr.append(" ".join(y))
        result = " 。 ".join(arr)

        print(result, file=ouf)
