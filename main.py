import json
import os
import multiprocessing

from predictor import Predictor

data_path = "/input"
output_path = "/output"
progress_path = "/progress"


def format_result(result):
    rex = {"accusation": [], "articles": [], "imprisonment": -3}

    res_acc = []
    for x in result["accusation"]:
        if not (x is None):
            res_acc.append(int(x))
    rex["accusation"] = res_acc

    if not (result["imprisonment"] is None):
        rex["imprisonment"] = int(result["imprisonment"])
    else:
        rex["imprisonment"] = -3

    res_art = []
    for x in result["articles"]:
        if not (x is None):
            res_art.append(int(x))
    rex["articles"] = res_art

    return rex


def update_progress(cnt):
    progress_file = open(os.path.join(progress_path, "res.txt"), "w")
    print(cnt, file=progress_file)
    progress_file.close()


if __name__ == "__main__":
    user = Predictor()
    cnt = 0


    def get_batch():
        v = user.batch_size
        if not (type(v) is int) or v <= 0:
            Ni_Mei_You_She_Zhi_Zheng_Que_De_batch_size

        return v


    def solve(fact):
        l = len(fact)
        result = user.predict(fact)

        if len(result) != l:
            Fan_Hui_De_Jie_Guo_Chang_Du_Bu_Deng_Yu_Gei_Ding_De_Shi_Shi_Chang_Du

        for a in range(0, len(result)):
            result[a] = format_result(result[a])

        return result


    for file_name in os.listdir(data_path):
        inf = open(os.path.join(data_path, file_name), "r")
        ouf = open(os.path.join(output_path, file_name), "w")

        fact = []

        for line in inf:
            fact.append(json.loads(line)["fact"])
            if len(fact) == get_batch():
                result = solve(fact)
                cnt += len(result)
                update_progress(cnt)
                for x in result:
                    print(json.dumps(x), file=ouf)
                fact = []

        if len(fact) != 0:
            result = solve(fact)
            cnt += len(result)
            update_progress(cnt)
            for x in result:
                print(json.dumps(x), file=ouf)
            fact = []

        ouf.close()
