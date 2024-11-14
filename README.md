# spotify-podcast-upload-checker

Spotify have very strict requirements for video to be added to podcast episodes.

[Full rules here](https://support.spotify.com/us/creators/article/video-specs/)

But they don't provide any feedback when an upload fails. So it's quite frustrating

So I had an idea to generate a quick script that uses ffprobe to check some of the key requirements. It's not checking everything but hopefully covers some of the main issues. 

I generated it then proof read it and tested it myself but not extensively so please chip in with any feedback.

## Prerequisites:
* Python
* FFmpeg

## How to run 
I'll *try* to make this do-able for a non-programmer but sorry if it's still not easy. ChatGPT should help. 

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
