# ffmpeg

#### 基本概念

- 流
    - 视频流
    - 音频流
    - 字幕流
        - 如果字幕流嵌入视频流就无法提取出来
- 分流
    - 将多个流从一个视频中对应提取出来
- 混流
    - 将多个流梳理之后写入一个视频
- 容器
    - 某种扩展# 基本概念

    - 流
        - 视频流
        - 音频流
        - 字幕流
            - 如果字幕流嵌入视频流就无法提取出来
    - 分流
        - 将多个流从一个视频中对应提取出来
    - 混流
        - 将多个流梳理之后写入一个视频
    - 容器
        - 某种扩展名类型的文件
- 编码
    - 将流用某种规范记录下来
- 解码
    - 将流还原
- 色深位
    - 颜色分级把纯黑到纯白分为 256 级，8 位色深度
- 色度采集
    - 视频录制和编码

### 命令

##### 隐藏开头打印信息

`-hide_banner`

##### 格式转换

```bash
ffmpeg -i video.flv video.mp4
# 显式指定编码器
# v 表示 video; a 表示 audio
ffmpeg -i video.flv -c:v libx264 -c:a flac video.mkv
```

##### 流复制

如果所有流都不改动输出的格式支持输入所有的流，可以直接复制流

```bash
ffmpeg -i video.avi -c copy video.mp4
```

##### 提取流

```bash
ffmpeg -i video.mp4 -c:a copy audio.aac
# 提取流时转码
ffmpeg -i video.mkv -c:a libmp3lame -q:a 2 audio.mp3
# 内挂字幕，将其字幕单独提取
ffmpeg -i video.mkv -c:s copy subtitle.srt
```
> 如果音频流和容器冲突，需要改为正确的编码器，或者让程序自己选择

##### 截取视频

视频的截取可以分为截取视频和截取图片

```bash
# 截取图片
ffmpeg -ss 3.5 -i video.mp4 -frames:v 1 extract.png
# 截取视频片段
ffmpeg -ss 00:02:00 -i video.mp4 -t 180 cut.mp4
```

##### 分辨率改变和缩放

分辨率改变需要使用到 `ffmpeg` 提供的视频过滤器 `video filter`

```bash
# 默认 bicubic 算法，缩放到高 720
ffmpeg -i video.mp4 -vf scale=-1:720 out.mp4
# 自动检测黑边区域裁剪
ffmpeg -i video.mp4 -vf "cropdetect" -c:a copy out.mp4
```

##### 设置视频预览图

```bash
# 设置预览图
ffmpeg -i video.mp4 -i thumb.png -map 0 -map 1 -c copy -c:v:1 png -disposition:v:1 attached_pic out.mp4
```

##### 视频变速

视频变速常用的应用场景是帧率减半，原理是将视频输出为不包含时间戳的数据流，然后重新封装时指定变速后的时间戳

##### 字幕操作

独立的字幕需要使用 `UTF-8` 编码
内挂字幕本质上是将字幕文件单独作为字幕流封装，因此不需要对视频流进行编码，可以选择开启或者关闭
内嵌字幕，将字幕与图像混叠的一种字幕，直接嵌入图像中，无法关闭

##### 合并视频

将待合并的视频文件路径依次列在一个 `txt` 文件中，然后 `ffmpeg` 读取

```bash
ffmpeg -f concat -i mylist.txt -c copy output.mp4
```

##### 删除流替换流

##### 压制和码率

- `CRF`
    - 恒定率系数，提供几种预案，预案越慢压制效果越好
- 二压
    - 强制要求文件大小
- 定限码率压制
    - 不要求文件大小，只是限制文件码率，主要用于网络传输

