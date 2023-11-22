import json
import os
import shutil

config = json.load(open("config.json", "r"))


def iterate_dir(direct):
    try:
        for filename in os.listdir(direct):
            if filename.endswith(".txt"):
                with open(os.path.join(direct, filename)) as f:
                    streak = 0
                    try:
                        lines = f.readlines()
                    except UnicodeDecodeError or PermissionError:
                        return False
                    lines_obj = enumerate(lines)
                    if len(lines) > 0:
                        for i, line in lines_obj:
                            line = line.strip()
                            if i > 0 and len(line) > 0 and lines[i - 1][0].isnumeric() and line[0].isnumeric() and int(
                                    line[0]) == int(lines[i - 1][0]) + 1:
                                streak += 1
                            elif len(line) > 0 and line[0] == "1":
                                streak += 1
                            else:
                                streak = 0
                        if streak >= config["highest_list"]:
                            print(os.path.abspath(os.path.join(direct, filename)))
                            shutil.copy(os.path.join(direct, filename), os.path.join(config["output"], filename))
            elif os.path.isdir(os.path.join(direct, filename)):
                iterate_dir(os.path.join(direct, filename))
    except PermissionError:
        return False


iterate_dir(config["target_dir"])
