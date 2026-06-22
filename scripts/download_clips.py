"""
download_clips.py

Downloads video(s) from a URL (single video, playlist, or channel) using yt-dlp.

Dependencies:
    - yt-dlp must be installed and available on PATH (pip install yt-dlp)
    - ffmpeg must be installed and on PATH (required by yt-dlp to merge audio/video)

Usage:
    python download_clips.py <url> [--out OUTPUT_DIR] [--max MAX_VIDEOS] [--quality HEIGHT]

Arguments:
    url          Video, playlist, or channel URL to download from
    --out        Output directory for downloaded files (default: ./downloads)
    --max        Max number of videos to download from a playlist/channel (default: all)
    --quality    Max video height in pixels, e.g. 720 or 1080 (default: 720)

Output:
    Downloaded video files (.mp4) saved to the output directory, named
    "<upload_date>_<title>.mp4". A matching .info.json metadata file is
    saved alongside each video (from --write-info-json).

Example:
    python download_clips.py "https://www.youtube.com/watch?v=XXXXXXXX" --out ./downloads --quality 1080
"""

import os
import sys
import subprocess
import argparse


def download_videos(url, output_dir, max_videos=None, quality="720"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cmd = [
        "yt-dlp",
        "-f", f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
        "-o", f"{output_dir}/%(upload_date)s_%(title)s.%(ext)s",
        "--merge-output-format", "mp4",
        "--write-info-json",
        "--restrict-filenames",
    ]

    if max_videos:
        cmd += ["--playlist-end", str(max_videos)]

    cmd.append(url)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"download failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("url", help="playlist or channel url")
    p.add_argument("--out", default="./downloads")
    p.add_argument("--max", type=int, default=None)
    p.add_argument("--quality", default="720")
    args = p.parse_args()

    download_videos(args.url, args.out, args.max, args.quality)
