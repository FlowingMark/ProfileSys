from pathlib import Path


def findAllFuncIdMap(log_path, out_map):
    path_profile_logs_dir = Path(log_path)
    func_files = [log for log in path_profile_logs_dir.rglob("func_dict*.log")]
    for file_tmp in func_files:
        file = file_tmp.open();
        for line in file.readlines():
            if (len(line) > 0):
                func_id_ref = line.split(" - ")
                func_num = int(func_id_ref[0])
                out_map[func_num] = func_id_ref[1]
        file.close();


def AnaFile(file_log, in_func_map, frame_num, big_num):
    with open(file_log) as f:
        func_map = dict()
        lines = f.readlines()
        for line in lines:
            num_list = line.split("\t")
            if (len(num_list) == 2):
                func_id = int(num_list[0])+1000001
                times = int(num_list[1])
                if (times > 0):
                    func_map[func_id] = times;
        result = sorted(func_map.items(), key = lambda x:x[1], reverse=True)
        out_file = file_log + "ana";
        out_80_file = out_file+".biglog"
        big_80_func_file = open(out_80_file, "w");
        with open(out_file, "w") as out_f:
            for key, value in result:
                out_line = str(key)+"\t"+str(value)+"\t"
                time_per_frame = value / frame_num;
                if(time_per_frame > big_num):
                    print(str(key), file=big_80_func_file)
                out_line += str(time_per_frame)
                if key in in_func_map.keys():
                    out_line =out_line +"\t"+ in_func_map[key]
                out_line = out_line.strip()
                print(out_line, file= out_f)
        big_80_func_file.flush();
        big_80_func_file.close();

out_dict = dict();
findAllFuncIdMap(r"D:\CodeBank\note-1\工作笔记\对局卡顿\tools\codeInsert\logs2",out_dict)
#AnaFile(r"G:\profile007\profile2\profileEngineFunc\ProfileTestFuncTimes1720497076.log", out_dict, 5794, 30.0)
#AnaFile(r"G:\profile007\profile2\profileEngineFunc\ProfileTestFuncTimes1720507285.log", out_dict, 7668, 30.0)
#AnaFile(r"G:\profile007\profile2\profileEngineFunc\ProfileTestFuncTimes1720508950.log", out_dict, 6952, 30.0)
#AnaFile(r"G:\profile007\profile2\profileEngineFunc\ProfileTestFuncTimes1720511073.log", out_dict, 13426, 30.0)
AnaFile(r"G:\profile007\profile2\profileEngineFunc\ProfileTestFuncTimes1720514245.log", out_dict, 10688, 30.0)
