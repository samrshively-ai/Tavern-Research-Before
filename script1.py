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
