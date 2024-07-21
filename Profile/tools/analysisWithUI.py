import os
import sys

import addFuncName
import resultAna
import treePlot
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import (QDropEvent, QFont, QIcon, QIntValidator, QKeyEvent,
                         QWheelEvent)
from PyQt5.QtWidgets import (QApplication, QComboBox, QFileDialog, QGridLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)


class FrameDataList:
    def __init__(self):
        self.cache_ids = list()
        self.index = 0
        self.origin_ids = list()
    
    def getPreId(self):
        if (self.cache_ids.__len__() == 0):
            return "no found";
        self.index -= 1
        if self.index < 0:
            self.index = self.cache_ids.__len__()-1
        return self.cache_ids[self.index]

    def getNextId(self):
        if (self.cache_ids.__len__() == 0):
            return "no found";
        self.index += 1
        if self.index >= self.cache_ids.__len__():
            self.index = 0
        return self.cache_ids[self.index]

    def applyFilter(self, filter_min):
        self.index = 0
        self.cache_ids.clear();
        for line in self.origin_ids:
            line_list = line.split("\t")
            if int(line_list[1]) >= filter_min:
                self.cache_ids.append(line)
        if (len(self.cache_ids) > 0):
            return self.cache_ids[0]
        return "no found >=  "+str(filter_min)
    
    def initFile(self, file):
        self.cache_ids.clear();
        self.origin_ids.clear();
        self.index = 0
        with open(file) as f:
            lines = f.readlines();
            line_num = 0
            for line in lines:
                line_num +=1
                line = line.strip();
                index = line.find("start=")
                if index != -1:
                    line = str(line_num) + " " +line
                    self.origin_ids.append(line)
        return self.applyFilter(0)
    
    def getCurCacheInfo(self):
        return len(self.cache_ids), self.index

class CustomLineEdit(QLineEdit):
    scroll_id_sig = pyqtSignal(bool)
    def __init__(self, str, parent = None):
        super(CustomLineEdit, self).__init__(str, parent)
        #self.setValidator(QIntValidator())
        self.setAcceptDrops(True)

    def keyPressEvent(self, e : QKeyEvent):
        if e.key() == Qt.Key.Key_Up or e.key() == Qt.Key.Key_Down:
            self.scroll_id_sig.emit(e.key() == Qt.Key.Key_Up)
        else:
            QLineEdit.keyPressEvent(self, e)

    def wheelEvent(self, e : QWheelEvent):
        if e.angleDelta().y() > 0 or e.angleDelta().y() < 0:
            self.scroll_id_sig.emit(e.angleDelta().y() > 0)

    def dropEvent(self, e : QDropEvent):
        pass
    def setNoCanFocus(self):
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

class DemoWnd(QWidget):
    def __init__(self):
        super(DemoWnd, self).__init__()
        self.window().setFixedHeight(360)
        self.window().setFixedWidth(900)
        self.frame_cache = FrameDataList()
        self.setWindowTitle("CodeAna")

        font = QFont("Rod", 14)
        self.label_res_path = QLabel("字典路径：", self)
        self.label_res_path.setFont(font)
        self.txt_res_path = CustomLineEdit("", self)
        self.txt_res_path.setNoCanFocus()
        self.go_res_path = QPushButton("选择路径", self)
        self.go_res_path.clicked.connect(self.go_res_path_clicked)

        self.label_id = QLabel("分析文件：", self)
        self.label_id.setFont(font)
        self.txt_id = CustomLineEdit("", self)
        self.txt_id.setNoCanFocus()
        self.go = QPushButton("选择文件", self)
        self.go.clicked.connect(self.select_file_clicked)
        self.sys_open_file = QPushButton("打开文件", self)
        self.sys_open_file.clicked.connect(self.sys_open_file_clicked)

        self.frame_name = QLabel("Frame：", self)
        self.frame_name.setFont(font)
        self.frame_desc = CustomLineEdit("", self)
        self.frame_desc.scroll_id_sig.connect(self.scroll_id)
        self.frame_desc.returnPressed.connect(self.go_clicked)
        #self.frame_desc.setNoCanFocus()
        self.frame_go = QPushButton("图示", self)
        self.frame_go.clicked.connect(self.go_clicked)

        self.frame_min_desc = QLabel("过滤最小帧时间：", self)
        self.frame_min_desc.setFont(font)
        self.frame_min = CustomLineEdit("", self)
        self.frame_min.returnPressed.connect(self.go_min_clicked)
        self.frame_min_go = QPushButton("应用过滤", self)
        self.frame_min_go.clicked.connect(self.go_min_clicked)

        self.frame_total = QLabel("总数：", self)
        self.frame_total.setFont(QFont("Rod",  18))
        self.frame_cur = QLabel("当前：", self)
        self.frame_cur.setFont(QFont("Rod",  18))

        self.game_time = QLabel("游戏时间：", self)
        self.game_time.setFont(QFont("Rod", 16))
        self.frame_time = QLabel("当前帧耗时：", self)
        self.frame_time.setFont(QFont("Rod", 16))

        self.grid_layout = QGridLayout()
        start_index = 0
        self.grid_layout.addWidget(self.label_res_path, start_index, 0)
        self.grid_layout.addWidget(self.txt_res_path, start_index, 1)
        self.grid_layout.addWidget(self.go_res_path, start_index, 2)
        start_index+= 1
        self.grid_layout.addWidget(self.label_id, start_index, 0)
        self.grid_layout.addWidget(self.txt_id, start_index, 1)
        self.grid_layout.addWidget(self.go, start_index, 2)
        self.grid_layout.addWidget(self.sys_open_file, start_index, 3)

        start_index+= 1
        self.grid_layout.addWidget(self.frame_name, start_index, 0)
        self.grid_layout.addWidget(self.frame_desc, start_index, 1)
        self.grid_layout.addWidget(self.frame_go, start_index, 2)

        start_index+= 1
        self.grid_layout.addWidget(self.frame_min_desc, start_index, 0)
        self.grid_layout.addWidget(self.frame_min, start_index, 1)
        self.grid_layout.addWidget(self.frame_min_go, start_index, 2)

        start_index+= 1
        self.grid_layout.addWidget(self.game_time, start_index, 0)
        self.grid_layout.addWidget(self.frame_time, start_index, 1)

        start_index+= 1
        self.grid_layout.addWidget(self.frame_total, start_index, 0)
        self.grid_layout.addWidget(self.frame_cur, start_index, 1)
 
        self.setLayout(self.grid_layout)
        self.setAcceptDrops(True)

    def select_file_clicked(self):
        file_name = self.txt_id.text()
        if (file_name == ""):
            file_name = r"G:\profile007\profile2"
        fileName1, filetype = QFileDialog.getOpenFileName(self,"选取文件", file_name,"frame Files (ProfileTest*.log)") #设置文件扩展名过滤,注意用双分号间隔
        print(fileName1,filetype)
        if len(fileName1)  >  0:
            or_file = ""
            func_file = ""
            if (fileName1[-9:] != "frame.log"):
                if (fileName1[-8:] == "func.log"):
                    func_file = fileName1
                    or_file = fileName1[:-8] + ".log"
                    fileName1 = fileName1[:-8] + "frame.log"
                else:
                    or_file = fileName1
                    func_file = fileName1[:-4] + "func.log"
                    fileName1 = fileName1[:-4] + "frame.log"
            else:
                func_file = fileName1[:-9] + "func.log";
                or_file = fileName1[:-9] + ".log"
            fuct_dict_dir = self.txt_res_path.text()
            if (not os.path.exists(func_file)):
                addFuncName.processOneLog(or_file,fuct_dict_dir)
            if (not os.path.exists(fileName1)):
                resultAna.processOneFile(or_file, fileName1, 15000)

            self.txt_id.setText(fileName1)
            self.frame_desc.setText(self.frame_cache.initFile(fileName1))
            self.frame_min.setText("0")
            self.updateFilterDesc()

    def sys_open_file_clicked(self):
        file_name = self.txt_id.text()
        if len(file_name) > 0:
            os.startfile(file_name)

    def scroll_id(self, up):
        if up:
            self.frame_desc.setText(self.frame_cache.getPreId())
        else:
            self.frame_desc.setText(self.frame_cache.getNextId())
        self.updateFilterDesc()

    def go_clicked(self):
        str_txt = self.frame_desc.text()
        index_1 = str_txt.find("start=")
        index_2 = str_txt.find(", end=")
        if (index_1 != -1 and index_2 != -1):
            start = int(str_txt[index_1+6:index_2])
            end = int(str_txt[index_2+6:])
            file = self.txt_id.text()
            file = file[:-9] + "func.log"
            print(file)
            treePlot.main(file=file, start=start, end=end)

    def go_min_clicked(self):
        str_txt = self.frame_min.text()
        if not str_txt.isdigit():
            print("input not allowed!!")
            QMessageBox.information(self, "WARNING", "输入的不是数字！！！")
            return
        self.frame_desc.setText(self.frame_cache.applyFilter(int(str_txt)))
        self.updateFilterDesc()

    def updateFilterDesc(self):
        total, curt = self.frame_cache.getCurCacheInfo();
        curt += 1
        self.frame_total.setText("总数："+str(total))
        self.frame_cur.setText("当前："+str(curt))
        str_txt = self.frame_desc.text()
        str_list = str_txt.split("\t");
        if len(str_list) >= 4:
            str_time = str_list[1] + "us"
            str_game_time = str_list[3]
            game_time = float(str_game_time)
            game_time /= 1000000.0
            str_game_time = "{:.2f}".format(game_time) + "s"
            self.frame_time.setText("当前帧耗时："+str_time);
            self.game_time.setText("游戏时间："+str_game_time);
    
    def go_res_path_clicked(self):
        file_path = self.txt_res_path.text()
        if len(file_path) == 0:
            file_path = "C:/"
        file_path_result = QFileDialog.getExistingDirectory(self,"选取字典文件夹", file_path) 
        if(len(file_path_result) != 0):
            self.txt_res_path.setText(file_path_result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DemoWnd()
    demo.show()
    sys.exit(app.exec())
