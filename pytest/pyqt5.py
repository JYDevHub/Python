import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from tkinter import filedialog
from tkinter import messagebox

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("pytest\pyqt5.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.CreateFld.clicked.connect(self.crtFld)
        self.DelFld.clicked.connect(self.delFld)
        self.SrcFld.clicked.connect(self.srcFld)
        self.imgbtn.clicked.connect(self.loadimg)
        
    def crtFld(self):
        print("폴더 생성")
        
    def delFld(self):
        print("폴더 삭제")
        
    def srcFld(self):
        print("폴더 찾기")
        
    def loadimg(self):
        self.qPixmapVar = QPixmap()
        
        imgpath = filedialog.askopenfilename(initialfile="/",\
                                title = "이미지 선택")
        self.qPixmapVar.load(imgpath)
        
        dir = "C:/Users/covin/Desktop/hdev/img"
        
        # for file in os.listdir(dir):
        #    i= 0
        #    self.qPixmapVar = QPixmap(os.path.join(dir, file))
        #    self.imglabel.resize(250, 200)
        #    self.imglabel.move(20+i,90)
        #    i += 250
        
        
        #self.imglabel.setPixmap(self.qPixmapVar)
        
        self.imglabel.setPixmap(self.qPixmapVar)
        
        
        imgpath = filedialog.askopenfilename(initialfile="/",\
                                title = "이미지 선택")
        self.qPixmapVar.load(imgpath)
        self.imglabel.move(400,180)
        self.imglabel.setPixmap(self.qPixmapVar)
    
        
if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스 
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()