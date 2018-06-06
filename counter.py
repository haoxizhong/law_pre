# coding: UTF-8

import os
import json
import re
from net.parser import ConfigParser

from net.data_formatter import get_time_id, check_sentence
from net.loader import get_name

in_path = r"/data/disk1/private/zhonghaoxi/cail/data/small"
out_path = r"/disk/mysql/law_data/count_data"

num_file = 20
num_process = 1

total_cnt = 0

crit = {}
law = {}
term = {}
fact_len = {}
sent_len = {}

config = ConfigParser("/home/zhx/law_pre/config/default_config.config")


def analyze_law(data):
    for x in data:
        if not (x in law.keys()):
            law[x] = 0
        law[x] += 1


def analyze_crit(data):
    for x in data:
        if not (x in crit.keys()):
            crit[x] = 0
        crit[x] += 1


def analyze_time(data):
    if data["death"]:
        data = 302
    elif data["forever"]:
        data = 303
    else:
        data = data["imprisonment"]
    if not (data in term.keys()):
        term[data] = 0
    term[data] += 1


def analyze_fact(data):
    l = len(data)
    if not (l in fact_len):
        fact_len[l] = 0
    fact_len[l] += 1

    l = 0
    for a in range(0, len(data)):
        l = max(l, len(data[a]))
    if not (l in sent_len):
        sent_len[l] = 0
    sent_len[l] += 1


def count(data):
    global total_cnt
    total_cnt += 1

    analyze_law(data["law"])
    analyze_crit(data["crit"])
    analyze_time(data["time"])
    analyze_fact(data["fact"])


def draw_out(in_path, out_path):
    print(in_path)
    inf = open(in_path, "r")

    cnt = 0
    for line in inf:
        data = json.loads(line)
        # if not (check(data)):
        #    continue
        # if not (check_sentence(data["content"], config)):
        #    continue
        count(data["meta"])
        cnt += 1
        if cnt % 500000 == 0:
            print(cnt)


def work(from_id, to_id):
    for a in range(int(from_id), int(to_id)):
        print(str(a) + " begin to work")
        draw_out(os.path.join(in_path, str(a)), os.path.join(out_path, str(a)))
        print(str(a) + " work done")


if __name__ == "__main__":
    work(0, 20)
    print(total_cnt)

    f = open(os.path.join(in_path, "crit.txt"), "w")
    x = 0
    while True:
        try:
            print(x, crit[x], file=f)
        except Exception as e:
            break
    f.close()

    f = open(os.path.join(in_path, "time.txt"), "w")
    x = 0
    while True:
        try:
            print(x, term[x], file=f)
        except Exception as e:
            break
    f.close()

    f = open(os.path.join(in_path, "lawx.txt"), "w")
    x = 0
    while True:
        try:
            print(x, law[x], file=f)
        except Exception as e:
            break
    f.close()

    f = open(os.path.join(in_path, "docu.txt"), "w")
    x = 0
    while True:
        try:
            print(x, fact_len[x], file=f)
        except Exception as e:
            break
    f.close()

    f = open(os.path.join(in_path, "sent.txt"), "w")
    x = 0
    while True:
        try:
            print(x, sent_len[x], file=f)
        except Exception as e:
            break
    f.close()

    f = open(os.path.join(in_path, "total.txt"), "w")
    print(total_cnt, file=f)
    f.close()
