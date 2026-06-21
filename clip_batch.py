import csv
import subprocess
import sys
import os
from pathlib import Path


def trim_clip(source_path, start, end, out_path):
    cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(start),
        "-to", str(end),
        "-i", source_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "fast",
        out_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def process_csv(csv_path, source_dir, out_dir):
    """
    csv columns expected: source_file, start, end, label
    times can be seconds or HH:MM:SS
    """
    os.makedirs(out_dir, exist_ok=True)

    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            src = os.path.join(source_dir, row["source_file"])
            if not os.path.exists(src):
                print(f"skipping row {i}: {src} not found")
                continue

            label = row.get("label", f"clip_{i}").replace(" ", "_")
            out = os.path.join(out_dir, f"{label}.mp4")
            print(f"trimming {src} [{row['start']} -> {row['end']}] -> {out}")
            try:
                trim_clip(src, row["start"], row["end"], out)
            except subprocess.CalledProcessError as e:
                print(f"  failed: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python clip_batch.py <csv> <source_dir> <out_dir>")
        sys.exit(1)
    process_csv(sys.argv[1], sys.argv[2], sys.argv[3])
