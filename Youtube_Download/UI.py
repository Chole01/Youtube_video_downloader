import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
from Youtube_Downloader import DownLoader

WIDTH = 500
HEIGHT = 600

IMAGE = '.\\Imag\\Youtube_Icon.png'

class Main_Window(QWidget):
    def __init__(self):
        super(Main_Window,self).__init__()
        self.resize(WIDTH,HEIGHT)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.UI()
    
    def UI(self):
        Window = QGroupBox(self)
        Window.resize(WIDTH,HEIGHT)
        Window.setStyleSheet("background-color:white;border-radius: 12px; border: 2px groove;")

        self.layout = QVBoxLayout(Window)

        self.Logo = QLabel(Window)
        self.image = QPixmap(IMAGE)
        self.image_resize = self.image.scaled(100,100)
        self.Logo.setPixmap(self.image_resize)
        self.Logo.setAlignment(QtCore.Qt.AlignmentFlag(4))
        self.Logo.setStyleSheet("background-color:white;border-radius: 12px; border: 0px groove;")

        self.progress_bar = QProgressBar(Window)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setFixedHeight(15)
        #self.progress_bar.setStyleSheet("background-color:white;border-radius: 12px; border: 0px groove;")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #FFFFFF;
                border: none;
                height: 10px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #98D3F5;
            }
        """)
        
        self.url_bar = QTextEdit(Window)
        self.url_bar.setFixedHeight(30)

        self.download_path = QTextBrowser(Window)
        self.download_path.setFixedHeight(30)

        self.url_hint = QLabel(Window)
        self.url_hint.setText("Here to input URL:")
        self.url_hint.setFont(QFont("helvetica", 13))
        self.url_hint.setStyleSheet("background-color:white;border-radius: 12px; border: 0px groove;")

        self.directory_hint = QLabel(Window)
        self.directory_hint.setText("Here to select download directory:")
        self.directory_hint.setFont(QFont("helvetica", 13))
        self.directory_hint.setStyleSheet("background-color:white;border-radius: 12px; border: 0px groove;")

        self.layout.addStretch(1)
        self.layout.addWidget(self.Logo)
        self.layout.addStretch(1)
        self.layout.addWidget(self.url_hint)
        self.layout.addWidget(self.url_bar)
        self.layout.addStretch(1)
        self.layout.addWidget(self.directory_hint)
        self.layout.addWidget(self.download_path)
        self.layout.addWidget(self.progress_bar)
        self.layout.addStretch(1)
        self.layout.addStretch(1)

        self.button_download = QPushButton("Download",Window)
        self.button_download.setFixedSize(100,45)
        self.button_download.move(100,HEIGHT-150)
        self.button_download.clicked.connect(self.Download)

        self.button_set_path = QPushButton("Set Directory",Window)
        self.button_set_path.setFixedSize(100,45)
        self.button_set_path.move(WIDTH-200,HEIGHT-150)
        self.button_set_path.clicked.connect(self.path_clicked)
        
    def path_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.download_path.setText(file_path)
            return file_path
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.mouse_press_px = e.globalPosition().x()
            self.mouse_press_py = e.globalPosition().y()

            self.delta_wx = self.mouse_press_px - self.geometry().x()
            self.delta_wy = self.mouse_press_py - self.geometry().y()
            
    def mouseMoveEvent(self, e):
        self.mouse_px = e.globalPosition().x()
        self.mouse_py = e.globalPosition().y()

        self.move(int(self.mouse_px - self.delta_wx), int(self.mouse_py - self.delta_wy))
            
    def Download(self):
        self.url_content = self.url_bar.toPlainText()
        self.download_directory = self.download_path.toPlainText()

        self.downloader = DownLoader(self.url_content,self.download_directory)
        self.downloader.trigger.connect(self.download_progress)
        self.downloader.start()
    
    def download_progress(self,progress):
        self.progress_bar.setValue(progress)
      
        
def main():
    app = QApplication(sys.argv)
    Window = Main_Window()
    Window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()