import os
import re
import sys
import time
from pathlib import Path

number_list = list()

def processPath(code_dir):
    path_profile_logs_dir = Path(code_dir)
    cpp_files = [log for log in path_profile_logs_dir.rglob("*.cpp")]
    for cpp_f in cpp_files:
        file_2_parse = cpp_f.open("r", -1, "gbk", errors="ignore");
        lines = file_2_parse.readlines();
        for lin in lines:
            index = lin.find("CGameProFile(")
            if index != -1:
                new_line = lin[index+13:]
                #print(new_line)
                index = new_line.find(")")
                new_line = new_line[:index]
                #print(new_line)
                number_list.append(int(new_line))
    number_list.sort()
    with open("tt.log", "w") as ff:
        for num in number_list:
            print(num, file=ff)


processPath(r"G:\master4test\depot")