import os
import sys

import numpy as np
import plotly.express as px

names = list()
parents = list()
values = list()

def addNameAndParent(name, par, value):
    names.append(name);
    parents.append(par);
    values.append(value);

def getFuncName(line_num , func_str, time, func_id):
    start = func_str.find(" ");
    end = func_str.find("(");
    func_name = func_str[start+1:end]
    if (start == -1 and end == -1):
        func_name= str(func_id)
    return str(line_num)+"_"+func_name+"_"+time

def searchParent(lines, line_num, end, child_start):
    for x in range(line_num , end):
        line = lines[x];
        line_list = line.split('\t')
        func_line = x+1   
        func_start_line = int(line_list[2])
        if (len(line_list) == 3):
            line_list.append("bool Frame()")
        if (func_start_line <= child_start):
            func_name = getFuncName(func_line, line_list[3], line_list[1], line_list[0])
            return func_name
    return ""

def anaOneFrame(lines, start , end ):
    for x in range(start , end):
        line = lines[x];
        line_list = line.split('\t')
        func_line = x+1
        func_start_line = int(line_list[2])
        if (len(line_list) == 3):
            line_list.append("bool Frame()")
        func_name = getFuncName(func_line, line_list[3], line_list[1], line_list[0])
        parent_name = ""
        if (line_list[0] != "-1"):
            parent_name = searchParent(lines, func_line, end, func_start_line)
        if (line_list[0] == "-999"):
            tmp_par_list = parent_name.split("_")
            line_list[1] = tmp_par_list[-1]
        addNameAndParent(func_name, parent_name, int(line_list[1]))
        


def main(file , start , end):
    names.clear()
    parents.clear()
    values.clear()
    with open(file) as f:
        lines = f.readlines();
        anaOneFrame(lines=lines, start=start, end=end);
    fig = px.treemap(names=names, parents=parents, values=values, color_discrete_sequence=["#FFA15A","#EF553B"])#
    px.colors.qualitative.Dark24
    fig.update_layout(font = dict(size = 16))
    fig.show()

if __name__ == "__main__":
    for i in range(1, len(sys.argv)):
        print('参数 %s 为：%s' % (i, sys.argv[i]))
    if len(sys.argv) < 4:
        print("未指定日志及开始结束行\n")
    else:
        tmp_path_log = sys.argv[1]
        tmp_start = sys.argv[2]
        tmp_end = sys.argv[3]
        main(file= tmp_path_log, start=tmp_start, end=tmp_end)
