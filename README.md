# LiveStream

📕中文说明 | [English](README.en.md)

LiveStream 是一个用于使用第三方播放器播放网络直播的命令行工具，可以读取直播流地址并提供给播放器进行播放，满足了非 Web/APP 环境下观看直播的需求。

LiveStream 本质上是一个 Shell 脚本，你可以直接查看脚本中的代码，并根据自己的需求进行 DIY。

本项目遵从 GPL 3.0 开源协议，仅用于个人学习用途，禁止各种形式的商用、盈利行为，禁止用于各种非法途径。

## 安装

你可以直接克隆此仓库，或者去 Release 下载最新的稳定版本。然后直接运行，或者将脚本放到 `$PATH` 路径下。

## 用法

你可以运行 `livestream -h` 去查看帮助：

```
LiveStream v0.0.1 Copyright © 2024-2026

Usage:
    livestream [options] [platform] [roomid]
    livestream [options] [url]

Supported platforms:
    bilibili, douyu

Basic Options:
    --debug               Enable debug mod.
    --cookie-from SOURCE  Read Bilibili cookies from a browser or Netscape cookie file.
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

- Bash、curl、jq
- Openssl
- Nodejs

## Bilibili 最高画质与登录

B 站接口会对未登录请求降低画质。脚本使用新版取流接口，按直播间各路流的
`accept_qn` 选择最高档位，并显示实际返回画质；如果服务端降级，会提示补充或刷新 Cookie。

使用可选参数 `--cookie-from <浏览器名或 Cookie 文件路径>` 提供登录态。
不带此参数时按匿名方式取流，不读取默认 Cookie 文件或环境变量。

```shell
# 使用 Firefox 当前的 B 站登录态
livestream --cookie-from firefox -p mpv bilibili 6

# 使用 Netscape 格式的 Cookie 文件
livestream --cookie-from "$HOME/path/to/cookies.txt" -p mpv bilibili 6

# 不使用 Cookie
livestream -p mpv bilibili 6
```

支持的浏览器名：`firefox`、`chrome`、`chromium`、`brave`、`edge`、`opera`、
`safari`、`vivaldi`、`whale`（取决于本机安装及系统支持）。
从浏览器读取需要 Python 3 及其 `yt-dlp` 包，会使用浏览器的默认配置选择方式，
只将未过期的 B 站 Cookie 保存到权限为 `0600` 的临时文件，取流后自动删除。
浏览器需要已登录 B 站；失效后在浏览器重新登录即可，无需单独刷新脚本。
从 Cookie 文件读取不需要 Python 或 yt-dlp，也不会修改原文件。

## 支持的平台

- Bilibili: 哔哩哔哩直播
- Douyu: 斗鱼直播

## 致谢

斗鱼的直播源解析规则参考了 [@wbt5](https://github.com/wbt5) 大佬的方法，特地在此表示感谢。

## 开源协议

[GPL-v3](LICENSE.md)
