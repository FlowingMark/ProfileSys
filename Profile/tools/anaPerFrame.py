
file_str = r"G:\master4test\exe\bin\ProfileTest1717492342.log";
with open("tmpPerFrame.log", "w") as log_file:
    with open(file_str) as f:
        frame_data_map = dict();
        for line in f.readlines():
            split = line.find('\t')
            if split > 0:
                key = line[0:split]
                time = str(line[split:-1])
                time = time.strip();
                time = int(time)
                key = key.strip();
                if(line[0:split] == "-1"):
                    for(m,n) in frame_data_map.items():
                        if(n > 0):
                            print(str(m)+" "+str(n), file=log_file)
                    print("frame end: " + str(time), file=log_file)
                    frame_data_map.clear();
                elif ((key) in frame_data_map.keys()):
                    frame_data_map[key] += time;
                else:
                    frame_data_map[key] = time;
