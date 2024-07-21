import os
import re
import sys
import time
from pathlib import Path

n_include_str ="#include"
include_str = "#include <platform/profile_sys/game_profile_sys.h>\n";
if_start_str = "#if"
if_end_str = "#endif"
slot_start_str = "/*"
slot_end_str = "*/"

def processPath(code_dir):
    path_profile_logs_dir = Path(code_dir)
    cpp_files = [log for log in path_profile_logs_dir.rglob("*.cpp")]
    first_include = -1;
    for cpp_f in cpp_files:
        file_2_parse = cpp_f.open("r", -1, "gbk", errors="ignore");
        lines = file_2_parse.readlines();
        line_num = 0
        header_line = -1
        has_if_start = 0
        need_chg_header = False
        to_insert_header_num = -1;
        for lin in lines:
            line_num += 1
            find_first_he = lin.find(n_include_str)
            if find_first_he != -1 and to_insert_header_num == -1:
                to_insert_header_num= line_num
            find_header = lin.find(include_str);
            find_if_start = lin.find(if_start_str)
            find_if_end = lin.find(if_end_str)
            if find_if_start != -1:
                has_if_start += 1
            if find_if_end != -1:
                has_if_start -= 1
            if find_header != -1:
                header_line = line_num
                if has_if_start > 0:
                    need_chg_header = True
                    break;
        if (need_chg_header):
            lines.remove(include_str)
            old_path_str = str(cpp_f.absolute())
            lines.insert(to_insert_header_num, include_str)
            print(to_insert_header_num)
            with open(old_path_str, "w") as ff:
                ff.writelines(lines);

def processPath2(code_dir):
    path_profile_logs_dir = Path(code_dir)
    cpp_files = [log for log in path_profile_logs_dir.rglob("*.cpp")]
    first_include = -1;
    for cpp_f in cpp_files:
        file_2_parse = cpp_f.open("r", -1, "gbk", errors="ignore");
        lines = file_2_parse.readlines();
        line_num = 0
        header_line = -1
        has_if_start = 0
        need_chg_header = False
        to_insert_header_num = -1;
        for lin in lines:
            line_num += 1
            find_first_he = lin.find(n_include_str)
            find_header = lin.find(include_str);
            find_if_start = lin.find(slot_start_str)
            find_if_end = lin.find(slot_end_str)
            if find_if_start != -1:
                has_if_start += 1
            if find_if_end != -1:
                has_if_start -= 1
            if find_header != -1:
                header_line = line_num
                if has_if_start > 0:
                    need_chg_header = True
            if find_first_he != -1 and to_insert_header_num == -1 and find_header == -1:
                to_insert_header_num= line_num
                break
        if (need_chg_header):
            lines.remove(include_str)
            old_path_str = str(cpp_f.absolute())
            lines.insert(to_insert_header_num-1, include_str)
            print(to_insert_header_num)
            with open(old_path_str, "w") as ff:
                ff.writelines(lines);



#processPath2(r"G:\testchgcPP")

processPath2(r"G:\master4test\depot\platform")
processPath2(r"G:\master4test\depot\products\Project_X52")