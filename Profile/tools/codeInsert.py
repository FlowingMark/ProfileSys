import os
import re
import sys
import time
from pathlib import Path

#func_pattern = re.compile(" [\w]*::[\w]*\(")
#func_pattern = re.compile("[\w]*::[\w]*\(")
func_pattern = re.compile("[\w]*::~*[\w]*\(")
include_pattern = re.compile("^#include")
include_str = "#include <platform/profile_sys/game_profile_sys.h>\n";
n_include_str ="#include"

func_id = 1;
gloablFuncMap = dict();

def getProfileFlag(num):
    profileFlag = "CGameProFile(";
    profileFlag += str(num);
    profileFlag += ")"
    return profileFlag;


def parseFile(path_file):
    global func_id;
    global gloablFuncMap;
    pre_func = ""
    print_file_once = False
    include_final_line_num = 0;
    line_num = 0
    wait_chg_line_map = dict()
    file = path_file.open("r", -1, "gbk", errors="ignore")
    f_list = file.readlines()
    pre_line = "";#上一行，用来判断是不是switch case; for; while
    to_insert_header_num = -1
    for line in f_list:
        line = line.strip()
        find_first_he = line.find(n_include_str)
        if find_first_he != -1 and to_insert_header_num == -1:
            to_insert_header_num= line_num
        match_func = func_pattern.search(line)
        if(match_func):
            tmp_line_func = line;
            if tmp_line_func[-1] != ";" and tmp_line_func[0:2] != "//" and tmp_line_func[0:2] != "if":
                if(pre_func != ""):
                    print("func no found impl :  "+ pre_func + " " + tmp_line_func);
                pre_func = tmp_line_func
        match_include = include_pattern.search(line);
        if(match_include):
            include_final_line_num = line_num;
        if (len(pre_func) > 0):
            tmp_line_func = line;
            pre_line_is_switch = False
            if (len(pre_line) > 6 and pre_line[:6] == "switch" ):
                pre_line_is_switch = True;
            if (len(pre_line) > 3 and pre_line[:3] == "for" ):
                pre_line_is_switch = True;
            if (len(pre_line) > 5 and pre_line[:5] == "while" ):
                pre_line_is_switch = True;
            if (len(pre_line) > 5 and pre_line[:5] == "class" ):
                pre_line_is_switch = True;
            if tmp_line_func[:1] == "{" and pre_line_is_switch == False:
                has_prof_flag = tmp_line_func.find("CGameProFile")
                if (has_prof_flag == -1):
                    func_id += 1;
                    tmp_list = list(line);
                    tmp_list.insert(1, getProfileFlag(func_id));
                    tmp_list.append("\n")
                    wait_chg_line_map[line_num] = "".join(tmp_list);
                    gloablFuncMap[func_id] = pre_func;
                pre_func = ""
        line_num += 1
        pre_line = line

    file.close();
    need_chg_file = False
    #添加 profile 打点
    for key in wait_chg_line_map.keys():
        f_list[key] = wait_chg_line_map[key];
        need_chg_file = True
    #添加头文件
    if (need_chg_file):
        f_list.insert(to_insert_header_num+1, include_str);
        old_path_str = str(path_file.absolute())
        with open(old_path_str, "w") as f:
            f.writelines(f_list);
        
def insertPath(code_dir):
    path_profile_logs_dir = Path(code_dir)
    cpp_files = [log for log in path_profile_logs_dir.rglob("*.cpp")]
    for file in cpp_files:
        file.chmod(0o777)
        #判断tui*res.cpp的文件不插入观察点
        file_name_str = file.name
        if (len(file_name_str)>10 and file_name_str[:3]=="tui" and file_name_str[-7:]=="res.cpp"):
            continue;
        parseFile(file);

def saveFuncDic(out_path): 
    timestamp = time.time()
    tmp_dir = out_path+"/"#"D:/CodeBank/note-1/工作笔记/对局卡顿/tools/codeInsert/logsogre/"
    file_out = tmp_dir + "func_dict";
    file_out += str(timestamp);
    file_out += ".log"
    with open(file_out, "w") as f:
        for key in gloablFuncMap.keys():
            print(str(key) + " - " + gloablFuncMap[key], file=f)

# for gameExample
def insertGameExample():
    global func_id
    global include_str;
    func_id = 1
    include_str = "#include \"../../../../include/game_profile_sys_helper.h\"\n"
    insertPath(r"D:\CodeBank\GitHub\ProfileSys\Profile\profile_sys\examples\GameExample\src")
    saveFuncDic(r"D:\CodeBank\GitHub\ProfileSys\Profile\profile_sys\bin")

insertGameExample()