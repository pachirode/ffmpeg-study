import sys

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QFrame, QProgressBar

from ui.page import Page


class MediaPage(Page):
    def __init__(self, parent=None):
        super(MediaPage, self).__init__(parent)

        self.start_stop_btn = None
        self.speed_box = None
        self.format_box = None
        self.exe_btn = None
        self.output_btn = None
        self.progress_bar = None
        self.displayer = None

        self.player = None
        self.audio_player = None
        self.video_player = None

        self.setup_ui()

    def setup_ui(self):
        self.setup_media_player()
        self.setup_tools()
        self.setup_process()

        self.init_tools()

    def setup_media_player(self):
        media_frame = QFrame(self)
        media_frame.setObjectName("mediaPlayerFrame")
        media_frame.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(media_frame)
        layout.setObjectName("mediaPlayerLayout")

        self.displayer = QWidget(media_frame)
        self.displayer.setObjectName("mediaPlayer")
        layout.addWidget(self.displayer)
        self.displayer.setVisible(False)

        self.player = QMediaPlayer()
        self.audio_player = QAudioOutput()
        self.video_player = QVideoWidget()
        self.player.setAudioOutput(self.audio_player)
        self.player.setVideoOutput(self.video_player)
        layout.addWidget(self.video_player)

        self.layout.addWidget(media_frame)

    def setup_tools(self):
        tool_frame = QFrame(self)
        tool_frame.setObjectName("mediaToolFrame")
        tool_frame.setFrameShape(QFrame.Shape.StyledPanel)

        tool_layout = QVBoxLayout(tool_frame)
        tool_layout.setObjectName("mediaToolLayout")

        control_layout = QHBoxLayout()
        control_layout.setObjectName("mediaControlLayout")

        self.start_stop_btn = QPushButton("播放/停止", tool_frame)
        speed_label = QLabel('Speed:')
        self.speed_box = QComboBox(tool_frame)
        format_label = QLabel('Format:')
        self.format_box = QComboBox(tool_frame)
        self.exe_btn = QPushButton('Execute')
        self.output_btn = QPushButton('Output')

        control_layout.addWidget(self.start_stop_btn)
        control_layout.addWidget(speed_label)
        control_layout.addWidget(self.speed_box)
        control_layout.addWidget(format_label)
        control_layout.addWidget(self.format_box)
        control_layout.addWidget(self.exe_btn)
        control_layout.addWidget(self.output_btn)

        tool_layout.addLayout(control_layout)

        self.layout.addWidget(tool_frame)

    def setup_process(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)

        self.layout.addWidget(self.progress_bar)

    def init_tools(self):
        self.speed_box.addItem("1")
        self.speed_box.addItem("1.5")
        self.speed_box.addItem("2")
        self.speed_box.addItem("2.5")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MediaPage()
    window.show()
    sys.exit(app.exec())
