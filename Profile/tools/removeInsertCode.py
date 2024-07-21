# 删除部分insert的标记

from pathlib import Path

profileFlag = "CGameProFile(";

def removeX52Engine(path):
    out_set = set()
    parseNeedRemoveFunc(r"D:\CodeBank\note-1\工作笔记\对局卡顿\tools\codeInsert\logs2", out_set=out_set)
    dir = path + "/";
    processPath(dir +"Base", out_set);
    processPath(dir +"InterfaceExImpl", out_set);
    processPath(dir +"InterfaceImpl", out_set);
    processPath(dir +"IOBinExporter", out_set);
    processPath(dir +"Level", out_set);
    processPath(dir +"LightShaft", out_set);
    processPath(dir +"Math", out_set);
    processPath(dir +"NewMaterial", out_set);
    processPath(dir +"OcclusionCulling", out_set);
    processPath(dir +"Phx", out_set);
    processPath(dir +"postprocess", out_set);
    processPath(dir +"RenderingPipeline", out_set);
    processPath(dir +"Resource", out_set);
    processPath(dir +"Scene", out_set);
    processPath(dir +"Selection", out_set);
    processPath(dir +"ShaderGenerator", out_set);
    processPath(dir +"specialeffect", out_set);


def processPath(code_dir, remove_funcid_set):
    path_profile_logs_dir = Path(code_dir)
    cpp_files = [log for log in path_profile_logs_dir.rglob("*.cpp")]
    for cpp_file in cpp_files:
        cpp_file.chmod(0o777)
        line_num = 0
        wait_chg_line = dict()
        file = cpp_file.open("r", -1, "gbk", errors="ignore")
        f_line_list = file.readlines()
        for f_line in f_line_list:
            index = f_line.find(profileFlag)
            if index != -1:
                new_tmp_line = f_line[index+13:]
                index_end = new_tmp_line.find(")")
                func_id = new_tmp_line[:index_end]
                if int(func_id) in remove_funcid_set:
                    wait_chg_line[line_num] = f_line[:index]+"\n"
            line_num += 1
        
        need_chg_file = False
        #添加 profile 打点
        for key in wait_chg_line.keys():
            f_line_list[key] = wait_chg_line[key];
            need_chg_file = True
        
        if (need_chg_file):
            old_path_str = str(cpp_file.absolute())
            with open(old_path_str, "w") as f:
                f.writelines(f_line_list);

def parseNeedRemoveFunc(dir_in, out_set):
    path_profile_logs_dir = Path(dir_in)
    log_files = [log for log in path_profile_logs_dir.rglob("*.biglog")]
    for log_file in log_files:
        with log_file.open() as f:
            for line in f.readlines():
                line = line.strip();
                out_set.add(int(line))

def processOnce():
    out_set = set()
    parseNeedRemoveFunc(r"D:\CodeBank\note-1\工作笔记\对局卡顿\tools\codeInsert\logs2", out_set=out_set)
    processPath(r"G:\profilecehua", out_set)

#processOnce()

removeX52Engine(r"F:\engine-35.9.0\Engine")