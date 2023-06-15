from pytube import YouTube
'''
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
'''
from PyQt6.QtCore import QThread, Qt, pyqtSignal

class DownLoader(QThread):
    trigger = pyqtSignal(int)
    
    def __init__(self,url,directory):
        super(DownLoader,self).__init__()
        self.url = url
        self.directory = directory
        self.youtube = YouTube(url,self.on_progress)

        self.stream = self.youtube.streams.get_highest_resolution()
    
    def run(self):
        self.stream.download(output_path=self.directory)

    def on_progress(self,stream, data_chunk, bytes_remaining):

        total_size = stream.filesize

        progress = int(100*(1- bytes_remaining/total_size))

        self.trigger.emit(progress)