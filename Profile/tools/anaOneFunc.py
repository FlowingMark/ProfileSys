from pathlib import Path


def processPath(code_dir, func_id):
    path_profile_logs_dir = Path(code_dir)
    log_files = [log for log in path_profile_logs_dir.rglob("ProfileTest17*.log")]
    max = 0;
    min = 9999;
    out_file_name = code_dir + "/" +str(func_id)+".funclog"
    with open(out_file_name, "w") as out_file:
        for log_file in log_files:
            file_name = log_file.name;
            if (file_name[-9:] == "frame.log" or file_name[-8:] == "func.log"):
                continue
            print(file_name, file=out_file)
            lines = log_file.open().readlines()
            for line in lines:
                word_list = line.split("\t")
                if (len(word_list) == 3 and int(word_list[0]) == func_id):
                    time = word_list[1]
                    print(time, file=out_file)

processPath(r"G:\profile007\profile2\p4", 339)