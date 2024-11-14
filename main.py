import json
import subprocess
import sys

def get_media_info(file_path):
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', 
           '-show_format', '-show_streams', file_path]
    
    try:
        output = subprocess.check_output(cmd)
        return json.loads(output)
    except subprocess.CalledProcessError:
        print(f"Error: Could not read file {file_path}")
        return None

def check_spotify_requirements(file_path):
    info = get_media_info(file_path)
    if not info:
        return
    
    issues = []
    
    # Check container format
    format_name = info['format']['format_name'].lower()
    if not ('mp4' in format_name or 'mov' in format_name):
        issues.append("❌ Container format must be MP4 or MOV")
    
    # Track count check
    video_streams = [s for s in info['streams'] if s['codec_type'] == 'video']
    audio_streams = [s for s in info['streams'] if s['codec_type'] == 'audio']
    
    if len(video_streams) != 1 or len(audio_streams) != 1:
        issues.append("❌ Must have exactly one video and one audio track")
    
    # Video checks
    if video_streams:
        video = video_streams[0]
        
        # Codec check
        codec_name = video['codec_name'].lower()
        if codec_name not in ['h264', 'hevc']:
            issues.append("❌ Video codec must be H.264 or H.265 (HEVC)")
        
        # Resolution check
        height = int(video['height'])
        if height != 1080:
            issues.append("❌ Video resolution must be 1080p")
        
        # Aspect ratio check
        width = int(video['width'])
        if round(width/height, 2) != 1.78:  # 16:9 = 1.78
            issues.append("❌ Aspect ratio must be 16:9")
        
        # Frame rate check
        fps = eval(video['r_frame_rate'])  # converts string fraction to float
        if fps < 24 or fps > 60:
            issues.append(f"❌ Frame rate must be between 24 and 60 fps (current: {fps:.2f} fps)")
        
        # Bitrate check (if available)
        if 'bit_rate' in video:
            bitrate_mbps = int(video['bit_rate']) / 1_000_000
            if height == 1080 and bitrate_mbps > 25:
                issues.append("❌ Bitrate exceeds 25 Mbps for 1080p")
            elif height > 1080 and bitrate_mbps > 35:
                issues.append("❌ Bitrate exceeds 35 Mbps for 4K")
    
    # Audio checks
    if audio_streams:
        audio = audio_streams[0]
        
        # Codec check
        codec_name = audio['codec_name'].lower()
        if codec_name not in ['aac', 'pcm_s16le', 'pcm_s24le']:
            issues.append("❌ Audio codec must be AAC-LC or PCM")
        
        # Channel check
        channels = int(audio['channels'])
        if channels != 2:
            issues.append("❌ Audio must be stereo (2 channels)")
        
        # Bitrate check (if available)
        if 'bit_rate' in audio:
            bitrate_kbps = int(audio['bit_rate']) / 1_000
            if bitrate_kbps < 192:
                issues.append("❌ Audio bitrate must be at least 192 Kbps")
    
    # Duration check
    duration = float(info['format']['duration'])
    if duration > 43200:  # 12 hours in seconds
        issues.append("❌ Duration exceeds 12 hours")
    
    # Print results
    if issues:
        print("\nThe following issues were found:")
        for issue in issues:
            print(issue)
    else:
        print("\n✅ Video meets all checked Spotify requirements!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_spotify_specs.py <video_file>")
        sys.exit(1)
    
    check_spotify_requirements(sys.argv[1])
