from pathlib import Path

frame_start_key = "-1";

def findLog( key_str, out_list, time_min, file_str):
    cur_time = 0;
    frame_span = 0;
    frame_per_second = 0;
    frame_time = 0;
    with open(file_str) as f:
        line_num = 0
        for line in f.readlines():
            line_num += 1
            line = line.strip()
            line_list = line.split('\t')
            if (line_list[0] == frame_start_key):
                cur_time += int(line_list[1])
                frame_span += 1;
                frame_time += int(line_list[1])
                frame_per_second += 1;
                if (frame_time > 1000000):
                    frame_time = frame_time - 1000000
                    tmp_fps="frame per second: "+str(frame_per_second);
                    out_list.append(tmp_fps)
                    frame_per_second = 0;
            if (line_list[0] == key_str):
                time = int(line_list[1])
                if time > time_min:
                    line = line + "\t" + str(cur_time)+ "\t"+str(frame_span) +"\t"+"start="+line_list[2]+", end="+str(line_num);
                    out_list.append(line);
                    frame_span = 0

def processOneFile(file_str, out_file, frame_lv):
    str_list = []
    findLog("-1", str_list, frame_lv, file_str=file_str);
    with open(out_file, "w") as log_file:
        for l in str_list:
            print(l, file=log_file)

def processDirFile(dir_str, frame_lv):
    path_profile_logs_dir = Path(dir_str)
    log_files = [log for log in path_profile_logs_dir.rglob("ProfileTest*.log")]
    for file_tmp in log_files:
        file_name = file_tmp.name;
        if (file_name[-8:] != "func.log" and file_name[-9:] != "frame.log"):
            file_full_path = file_tmp.absolute().__str__();
            file_name_list = file_full_path.split(".");
            file_name_list[0] +="frame"
            file_name_list[0] +=".log"
            processOneFile(file_full_path, file_name_list[0], frame_lv)


#processOneFile(r"G:\profile007\p1\ProfileTest1718939984.log", "tmp2.log", 30000)
#dir_str2 = r"G:\profile007\p2";
#dir_str3 = r"G:\profile007\p3";
#dir_str4 = r"G:\profile007\p4";
#dir_str5 = r"G:\profile007\p5";
#processDirFile(dir_str2, 30000);
#processDirFile(dir_str3, 30000);
#processDirFile(dir_str4, 30000);
#processDirFile(dir_str5, 30000);
#dir_str6 = r"G:\profile007\profile2\p33";
#dir_str6 = r"G:\profile007\profile2\p33\p33";
#processDirFile(dir_str6, 15000);