import os
import random

from net.parser import ConfigParser
from net.data_formatter import check_sentence

in_path = "/data/disk1/private/zhx/law/data/big"
out_path = "/data/disk1/private/zhx/law/data/big"


def solve_file(file_name, lower_bound, upper_bound):
    arr = []
    cnt = 0

    for a in range(lower_bound, upper_bound + 1):
        inf = open(os.path.join(in_path, str(a)), "r")

        for line in inf:
            try:
                cnt = cnt + 1
                arr.append(line[:-1])

            except Exception as e:
                print(e)
                gg
    print(len(arr))
    random.shuffle(arr)

    ouf = []
    for a in range(lower_bound, upper_bound + 1):
        ouf.append(open(os.path.join(out_path, str(a)), "w"))

    for a in range(0, len(arr)):
        print(arr[a], file=ouf[a % (upper_bound - lower_bound + 1)])


solve_file("train.json", 0, 14)
solve_file("test.json", 15, 19)
