import os
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout,
    QFileDialog
)

app = QApplication([])

#окно
win = QWidget()
win.setWindowTitle('Фотошоп на минималках')
win.resize(700,500)

#интрефейс
btn_folder = QPushButton('ПАПКА')
list_files = QListWidget()
image = QLabel('Картинка')

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Отзеркалить')
btn_rezcost = QPushButton('Резкость')
btn_gray = QPushButton('Ч\Б')

#расположение
main_layout = QHBoxLayout()
line_files = QVBoxLayout()
line_image = QVBoxLayout()
line_editor = QHBoxLayout()
line_files.addWidget(btn_folder)
line_files.addWidget(list_files)
line_image.addWidget(image)
line_editor.addWidget(btn_left)
line_editor.addWidget(btn_right)
line_editor.addWidget(btn_mirror)
line_editor.addWidget(btn_rezcost)
line_editor.addWidget(btn_gray)
main_layout.addLayout(line_files)
main_layout.addLayout(line_image)
line_image.addLayout(line_editor)

#фукционал
class Editor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.fullname = None

    def load_image(self,filename):
        self.filename = filename
        self.fullname = os.path.join(workdir,filename)
        self.image = Image.open(self.fullname)

    def show_image(self,dir):
        pixmap = QPixmap(dir)
        pixmap = pixmap.scaled(image.width(), image.height(), Qt.KeepAspectRatio)
        image.setPixmap(pixmap)

    def save_image(self):
        dir = os.path.join(workdir,'Mod/')
        if not os.path.exists(dir):
            os.mkdir(dir)
        fullname = os.path.join(dir,self.filename)
        self.image.save(fullname)

    def gray(self):
        self.image = self.image.convert('L')
        self.save_image()
        self.show_image(os.path.join(workdir,'Mod/',self.filename))

    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        self.show_image(os.path.join(workdir,'Mod/',self.filename))

    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        self.show_image(os.path.join(workdir,'Mod/',self.filename))

    def flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        self.show_image(os.path.join(workdir,'Mod/',self.filename))

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        self.show_image(os.path.join(workdir,'Mod/',self.filename))

   

  
def show_file():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    files = os.listdir(workdir)
    list_files.clear()
    for file in files:
        for ext in ['.jpg','.png']:
            if file.endswith(ext):
                list_files.addItem(file)

def show_chosen_image():
    filename = list_files.currentItem().text()
    work_image.load_image(filename)
    work_image.show_image(work_image.fullname)

#обьект редактора
work_image = Editor()
list_files.currentRowChanged.connect(show_chosen_image)

#подписки
btn_folder.clicked.connect(show_file)
btn_gray.clicked.connect(work_image.gray)
btn_left.clicked.connect(work_image.left)
btn_right.clicked.connect(work_image.right)
btn_mirror.clicked.connect(work_image.flip)
btn_rezcost.clicked.connect(work_image.sharpen)

#запуск приложения
win.setLayout(main_layout)
win.show()
app.exec()