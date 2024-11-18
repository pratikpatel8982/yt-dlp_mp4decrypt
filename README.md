This is a plugin for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that enables decryption of encrypted audio and video files using the `mp4decrypt` command-line tool. The files will be decrypted instantly after download and will replace the encrypted files.

## Prerequisites

Before using this plugin, ensure that you have the `mp4decrypt` executable added to your system's PATH. You can download the `mp4decrypt` tool from the [Bento4](https://www.bento4.com/) website and follow their installation instructions.

## Installation

You can install this plugin directly from the GitHub repository using the following command:

```shell
python -m pip install -U https://github.com/pratikpatel8982/yt-dlp-mp4decrypt/archive/master.zip
```

Make sure you have Python 3.6+ installed before running this command.

## Usage

To use this plugin, make sure you place the `--use-postprocessor` option before any other arguments to avoid any issues. Here are the correct usage instructions:

### Decrypt using a single decryption_key:

```shell
yt-dlp --use-postprocessor MP4Decrypt:decryption_key=your_key <video_url>
```

Replace `your_key` with your actual decryption key in the format `kid:key`.

### Decrypt using keys from `keys.txt`(Useful when downloading a Playlist):

```shell
yt-dlp --use-postprocessor MP4Decrypt:keyfile="/path/to/keys.txt" <video_url or playlist_url>
```

Replace `/path/to/keys.txt` with the actual path to your `keys.txt` file. Make sure `keys.txt` contains keys in the format `kid:key`, one per line. `mp4decrypt` will automatically decrypt the file using the correct `keys` from `keys.txt`

#### keys.txt Sample:
If you're decrypting using keys from a file, the `keys.txt` file should contain keys in the format `kid:key`, with each key on a separate line. Here's a sample `keys.txt` file:
```shell
kid1:key1
kid2:key2
kid3:key3
kid4:key4
kid5:key5
```
