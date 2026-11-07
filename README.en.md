# LiveStream

[中文说明](README.md) | 📕English

LiveStream is a CLI tool that uses third-party players to play network live.    It reads the live stream address and provides it to the player for playback, meeting the need for live streaming in environments that are not Web/APP-based.

LiveStream is essentially a shell script, and you can view the code directly within the script and customize it to meet your own needs.

This project complies with the GPL 3.0 open source license and is intended for personal learning purposes only.    All forms of commercial use, profit-making activities, and illegal uses are strictly prohibited.

## Installation

You can clone this repository directly, or download the latest stable version from the Release page. Then run it directly, or place the script in the `$PATH` directory. 

## Usage

You can run `livestream -h` to view the help: 

```
LiveStream v0.0.1 Copyright © 2024-2024

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

For example:
1. To watch the 12345678 live stream on Bilibili Live platform using VLC player, you can run: 

    ```shell
    livestream -p vlc bilibili 12345678
    ```

2. To watch `https://www.douyu.com/123456` with MPV player, you can run: 

    ```shell
    livestream -p mpv https://www.douyu.com/12345678
    ```

## Bilibili quality and login

Bilibili limits anonymous requests to lower quality. The script uses the newer
playback API, requests the highest quality advertised by this room's streams,
prints the actual quality, and warns if the server downgrades it.

Use the optional `--cookie-from <browser or cookie file path>` argument to
provide login cookies. Without it, requests are anonymous; no default cookie
file or cookie environment variable is read.

```shell
livestream --cookie-from firefox -p mpv bilibili 6
livestream --cookie-from "$HOME/path/to/cookies.txt" -p mpv bilibili 6
livestream -p mpv bilibili 6
```

Supported browser names: `firefox`, `chrome`, `chromium`, `brave`, `edge`, `opera`,
`safari`, `vivaldi`, and `whale`, subject to local installation and OS support.
Browser extraction requires Python 3 with the `yt-dlp` package. It uses yt-dlp's
default profile selection and saves only unexpired Bilibili cookies to a temporary
file with permissions `0600`, which is removed after fetching the stream URL.
Log in again in the browser when the session expires; no refresh script is needed.
Cookie files must use Netscape format and are read without modification. Reading
a cookie file requires neither Python nor yt-dlp.

## Dependencies

- Bash, curl, jq
- Openssl
- Nodejs

## Supported Platforms 

- Bilibili: Bilibili Live Streaming
- Douyu: Douyu Live Streaming 

## Thanks

The live stream source decoding rules of Douyu are based on the method of @wbt5, and I would like to express my gratitude here specially.

## Open Source LICENSE

[GPL-v3](LICENSE.md)
