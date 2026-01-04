import sys
import subprocess
import tempfile
import os

from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, QTimer


class VideoCutter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video/Audio Cutter")

        self.video_path = None
        self.temp_audio = None  # 临时 wav 文件路径

        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)

        self.load_btn = QPushButton("加载媒体")
        self.play_btn = QPushButton("播放 / 暂停")
        self.cur_btn = QPushButton("获取当前时间")
        self.cut_prev_btn = QPushButton("向前截取")
        self.cut_next_btn = QPushButton("向后截取")

        self.time_label = QLabel("当前时间：0.0 s")
        self.cut_len = QDoubleSpinBox()
        self.cut_len.setRange(0.1, 600.0)
        self.cut_len.setValue(5.0)
        self.cut_len.setDecimals(2)
        self.cut_len.setSuffix(" 秒")

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_widget)

        ctrl = QHBoxLayout()
        ctrl.addWidget(self.load_btn)
        ctrl.addWidget(self.play_btn)
        layout.addLayout(ctrl)

        cut_ctrl = QHBoxLayout()
        cut_ctrl.addWidget(QLabel("截取长度"))
        cut_ctrl.addWidget(self.cut_len)
        cut_ctrl.addWidget(self.cur_btn)
        cut_ctrl.addWidget(self.cut_prev_btn)
        cut_ctrl.addWidget(self.cut_next_btn)
        layout.addLayout(cut_ctrl)

        layout.addWidget(self.time_label)

        self.load_btn.clicked.connect(self.load_media)
        self.play_btn.clicked.connect(self.toggle_play)
        self.cur_btn.clicked.connect(self.set_cur)
        self.cut_prev_btn.clicked.connect(self.cut_prev)
        self.cut_next_btn.clicked.connect(self.cut_next)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(300)

    def load_media(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择媒体文件",
            "",
            "Media Files (*.mp4 *.mkv *.avi *.mp3 *.wav *.pm3)"
        )
        if not path:
            return

        self.video_path = path
        ext = os.path.splitext(path)[1].lower()

        if ext == ".pm3":
            self.video_widget.hide()
            self.load_pm3_as_audio(path)
        else:
            self.video_widget.show()
            self.player.setSource(QUrl.fromLocalFile(path))
            self.player.play()

    def load_pm3_as_audio(self, path):
        # 创建临时 wav 文件
        fd, wav_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        self.temp_audio = wav_path

        # ffmpeg 转码 pm3 -> wav
        cmd = [
            "ffmpeg",
            "-y",
            "-i", path,
            "-vn",
            "-acodec", "pcm_s16le",
            wav_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 播放临时 wav
        self.player.setSource(QUrl.fromLocalFile(wav_path))
        self.player.play()

    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def update_time(self):
        pos = self.player.position() / 1000.0
        self.time_label.setText(f"当前时间：{pos:.2f} s")

    def set_cur(self):
        self.cut_len.setValue(self.player.position() / 1000.0)

    def cut_prev(self):
        self.cut_video(forward=False)

    def cut_next(self):
        self.cut_video(forward=True)

    def cut_video(self, forward=True):
        if not self.video_path:
            return

        cur = self.player.position() / 1000.0
        length = self.cut_len.value()

        if forward:
            start = cur
        else:
            start = max(0, cur - length)

        output = "cut_output.mp4"

        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-i", self.video_path,
            "-t", str(length),
            "-c", "copy",
            output
        ]

        subprocess.Popen(cmd)

    def closeEvent(self, event):
        # 清理临时 wav 文件
        if self.temp_audio and os.path.exists(self.temp_audio):
            os.remove(self.temp_audio)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = VideoCutter()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec())
