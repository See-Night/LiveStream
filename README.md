# LiveStream

📕中文说明 | [English](README.en.md)

LiveStream 是一个用于使用第三方播放器播放网络直播的命令行工具，可以读取直播流地址并提供给播放器进行播放，满足了非 Web/APP 环境下观看直播的需求。

LiveStream 本质上是一个 Shell 脚本，你可以直接查看脚本中的代码，并根据自己的需求进行 DIY。

本项目遵从 GPL 3.0 开源协议，仅用于个人学习用途，禁止各种形式的商用、盈利行为，禁止用于各种非法途径。

## 安装

你可以直接克隆此仓库，或者去 Release 下载最新的稳定版本。然后直接运行，或者将脚本放到 `$PATH` 路径下。

## 用法

你可以运行 `livestream -h` 去查看帮助：

```shell
LiveStream v0.0.1 Copyright © 2024-2024

Usage:
    livestream [options] [platform] [roomid]
    livestream [options] [url]

Supported platforms:
    bilibili, douyu

Basic Options:
    -p,--player PLAYER    Play with the specified video player. Such as mpv, vlc, etc.
                          Or the path of player, such /path/to/player.
    -h, --help            Print help information
```

例如：
1. 要使用 VLC 播放器观看 Bilibili 直播平台的 12345678 直播间，你可以运行：

    ```shell
    livestream -p vlc bilibili 12345678
    ```

2. 要使用 MPV 播放器观看 `https://www.douyu.com/12345678`，你可以运行：

    ```shell
    livestream -p mpv https://www.douyu.com/12345678
    ```
## 依赖

- Openssl
- Nodejs

## 支持的平台

- Bilibili: 哔哩哔哩直播
- Douyu: 斗鱼直播

## 致谢

斗鱼的直播源解析规则参考了 [@wbt5](https://github.com/wbt5) 大佬的方法，特地在此表示感谢。

## 开源协议

[GPL-v3](LICENSE.md)
