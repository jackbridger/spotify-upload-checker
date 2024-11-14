# spotify-podcast-upload-checker

Spotify have very strict requirements for video to be added to podcast episodes.

## Container
* .MP4 or .MOV files
* Must have two tracks: one video and one audio
* The video and audio tracks must have the same duration
* Recommended bitrate of 25 Mbps for HD, or 35 Mbps for 4K

## Video

* H.264 high profile or H.265 (HEVC)
* 1080p resolution
* 16:9 widescreen aspect ratio
* Maximum bitrates of 25 Mbps for 1080p source, or 35 Mbps for 4k source
* Use a fixed frame rate between 24 to 60 frames per second
* Maximum duration of 12 hours
* Use 8-bit color depth and 4:2:0 subsampling

## Audio
* AAC-LC or PCM
* Bitrate of 192 Kbps or higher
* Stereo
* Surround/multi-channel audio is not supported
* Maximum duration of 12 hours


[https://support.spotify.com/us/creators/article/video-specs/](Full rules here)

But they don't provide any feedback when an upload fails. So it's quite frustrating

So I had an idea to generate a quick script that uses ffprobe to check some of the key requirements. It's not checking everything but hopefully covers some of the main issues. 

I've not tested it extensively so please chip in with any feedback.

## Prerequisites:
* Python
* FFmpeg

## How to run 
I'll *try* to make this do-able for a non-programmer but sorry if it's not easy. ChatGPT should help. 

1. Make sure you have python (or python3) and ffmpeg installed (type python or python3 in your terminal and press enter to test python. And ffmpeg to test ffmpeg/ffmprobe). If nothing happens you probably don't have them. 
2. Download the python file above and save it on your computer 
3. Open your terminal (on Mac type cmd-space and search terminal)
4. Navigate to where your python file is (e.g. type "cd Downloads")
5. Make sure your video is in the same folder
6. In your terminal, type ```python3 main.py *your_file_name* ```

E.g. a passing video is like
```
% python3 main.py Gonto\ Video.mp4 

✅ Video meets all checked Spotify requirements!
```

And a fail is like 

```
% python3 main.py homebrew.mov 

The following issues were found:
❌ Audio codec must be AAC-LC or PCM
```

```
% python3 main.py ghost.mp4 

The following issues were found:
❌ Frame rate must be between 24 and 60 fps (current: 23.98 fps)
```
Hope it's helpful!
