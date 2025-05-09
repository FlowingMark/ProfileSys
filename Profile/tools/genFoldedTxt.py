
names = list()
parents = list()
values = list()

func_parent_dict = dict()

def addNameAndParent(name, par, value):
    names.append(name);
    parents.append(par);
    values.append(value);
    func_parent_dict[name] = par

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

def makeStack(output_file):
    stack = list()
    not_leaf = set()
    with open(output_file, "w") as f:
        for x in range(len(names)):
            if (names[x] not in not_leaf):
                addStackParent(stack, names[x], not_leaf)
                stack.reverse()
                correct_stack = ";".join(stack)
                stack.clear()
                correct_stack = correct_stack + " " + str(values[x])
                print(correct_stack, file=f)

def addStackParent(stack, func_name, not_leaf):
    parent = func_parent_dict[func_name]
    if (parent != ""):
        stack.append(parent)
        not_leaf.add(parent)
        addStackParent(stack, parent, not_leaf)

def main(file, start, end):
    names.clear()
    parents.clear()
    values.clear()
    with open(file) as f:
        lines = f.readlines();
        anaOneFrame(lines=lines, start=start, end=end);
    makeStack("D:\\testflame.txt");


# test
main(r"G:\profile007\profile2\p2\ProfileTest1719986853func.log", 487158, 487978)