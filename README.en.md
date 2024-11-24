# LiveStream

[中文说明](README.md) | 📕English

LiveStream is a CLI tool that uses third-party players to play network live.    It reads the live stream address and provides it to the player for playback, meeting the need for live streaming in environments that are not Web/APP-based.

LiveStream is essentially a shell script, and you can view the code directly within the script and customize it to meet your own needs.

This project complies with the GPL 3.0 open source license and is intended for personal learning purposes only.    All forms of commercial use, profit-making activities, and illegal uses are strictly prohibited.

## Installation

You can clone this repository directly, or download the latest stable version from the Release page. Then run it directly, or place the script in the `$PATH` directory. 

## Usage

You can run `livestream -h` to view the help: 

```shell
LiveStream v0.0.1 Copyright © 2024-2024

Usage:
    livestream [options] [platform] [roomid]
    livestream [options] [url]

Supported platforms:
    Bilibili, Douyu

Basic Options:
    -p,--player PLAYER    Play with the specified video player. Such as mpv, vlc, etc.
                          Or the path of player, such /path/to/player.
    -h, --help            Print help information
```

For example:
1. To watch the 12345678 live stream on Bilibili Live platform using VLC player, you can run: 

    ```shell
    livestream -p vlc bilibili 12345678
    ```

2. To watch `https://www.douyu.com/123456` with MPV player, you can run: 

    ```shell
    livestream -p mpv https://www.douyu.com/12345678
    ```

## Dependencies 

- Python
- Nodejs

> [!NOTE]
These two scripts are mainly needed when decoding DouyuTV's live stream source, as DouyuTV's live stream source requires the platform's JavaScript script to run and needs to be encrypted with MD5. However, the encryption results obtained by using `md5sum` and OpenSSL are incorrect, so only Python's `hashlib` can be used for encryption. 

## Supported Platforms 

- Bilibili: Bilibili Live Streaming
- Douyu: Douyu Live Streaming 

## Thanks

The live stream source decoding rules of Douyu are based on the method of @wbt5, and I would like to express my gratitude here specially.

## Open Source LICENSE

[GPL-v3](LICENSE.md)
