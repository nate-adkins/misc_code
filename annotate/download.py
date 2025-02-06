import os
import subprocess

def download_youtube_video(url, output_dir="videos"):
    """Downloads a YouTube video using yt-dlp and returns the saved filename."""
    os.makedirs(output_dir, exist_ok=True)
    video_id = subprocess.run(
        ["yt-dlp", "--get-id", url], capture_output=True, text=True
    ).stdout.strip()
    if not video_id:
        print("Failed to retrieve video ID.")
        return None, None
    unique_folder = os.path.join(output_dir, video_id)
    os.makedirs(unique_folder, exist_ok=True)
    video_path = os.path.join(unique_folder, f"{video_id}.mp4")
    command = ["yt-dlp", "-f", "bestvideo+bestaudio", "--merge-output-format", "mp4", 
               "-o", video_path, url]
    print(f"Downloading video to: {video_path}")
    subprocess.run(command, check=True)
    return video_path, unique_folder

def extract_frames(video_path, output_folder, fps=1):
    """Extracts frames from video using ffmpeg."""
    os.makedirs(output_folder, exist_ok=True)
    frame_pattern = os.path.join(output_folder, "frame_%04d.jpg")
    ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")
    command = [ffmpeg_path, "-i", video_path, "-vf", f"fps={fps}", frame_pattern]
    print(f"Extracting frames to: {output_folder}")
    subprocess.run(command, check=True)
    
if __name__ == "__main__":
    yt_url = "https://www.youtube.com/watch?v=37mgZclglAA"
    video_path, folder = download_youtube_video(yt_url)
    if video_path:
        extract_frames(video_path, folder)
        print(f"Frames extracted in: {folder}")
    else:
        print("Download failed.")
