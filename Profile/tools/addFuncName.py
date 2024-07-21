from pathlib import Path


def processLog( file_str, in_func_map):
    with open(file_str) as f:
        func_out_line_list = list();
        func_line_list = f.readlines();
        for line in func_line_list:
            line = line.strip()
            line_list = line.split('\t')
            func_id = int(line_list[0])
            if func_id in in_func_map.keys():
                line =line +"\t"+ in_func_map[func_id]
            else:
                line = line+"\t"+"void "+str(func_id)+"()" # use func_id when has no dict
            line = line.strip()
            line += "\n"
            func_out_line_list.append(line)

        file_name_list = file_str.split(".");
        file_name_list[0] +="func"
        file_name_list[0] +=".log"
        with open(file_name_list[0], "w") as f_out:
            f_out.writelines(func_out_line_list);


def findAllFuncIdMap(log_path, out_map):
    if (len(log_path) > 0):
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
    if (-1 not in out_map):
        out_map[-1] = "void Frame()"
    if (-999 not in out_map):
        out_map[-999] = "void TriggerFuncTimes()"

def processDir(dir, fun_map, out_dict):
    path_profile_logs_dir = Path(dir)
    log_files = [log for log in path_profile_logs_dir.rglob("ProfileTest*.log")]
    for file_tmp in log_files:
        file_name = file_tmp.name;
        if (file_name[-8:] != "func.log" and file_name[-9:] != "frame.log"):
            full_path_file = file_tmp.absolute();
            processLog(full_path_file.__str__(), in_func_map=out_dict)


#out_dict = dict();
#findAllFuncIdMap(r"D:\CodeBank\note-1\工作笔记\对局卡顿\tools\codeInsert\logs2",out_dict)

#单个文件处理
#file_str = r"G:\profile007\ProfileTest1718881305.log";
#processLog(file_str=file_str, in_func_map=out_dict)

#文件夹内所有文件处理
#log_dir = r"G:\profile007\profile2\p33"
#log_dir = r"G:\profile007\profile2\p33\p33"
#processDir(log_dir, fun_map=out_dict)

def processOneLog(file, func_dict_path):
    out_dict = dict();
    findAllFuncIdMap(func_dict_path, out_dict)
    processLog(file_str=file, in_func_map=out_dict)