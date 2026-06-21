"""
batch_trim_clips.py

Batch-trims multiple clips out of source video file(s), driven by a CSV file
that lists what to cut and where. Uses ffmpeg to do the actual trimming.

Dependencies:
    - ffmpeg must be installed and available on PATH

Usage:
    python batch_trim_clips.py <csv_path> <source_dir> <out_dir>

Arguments:
    csv_path     Path to a CSV with columns: source_file, start, end, label
                 - source_file: filename of the source video, relative to source_dir
                 - start, end: timestamps, either seconds (e.g. "12.5") or
                   HH:MM:SS (e.g. "00:01:23")
                 - label: name for the output clip (spaces will be replaced
                   with underscores); if omitted, defaults to "clip_<row index>"
    source_dir   Directory containing the source video files referenced in the CSV
    out_dir      Directory where trimmed output clips will be written
                 (created automatically if it doesn't exist)

Output:
    One .mp4 file per CSV row, written to out_dir, named "<label>.mp4".
    Rows whose source_file can't be found are skipped (logged, not fatal).
    Rows that fail during ffmpeg trimming are logged and skipped; the rest
    of the batch continues.

Example:
    python batch_trim_clips.py clips_to_cut.csv ./raw_footage ./trimmed
"""

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
        print("usage: python batch_trim_clips.py <csv> <source_dir> <out_dir>")
        sys.exit(1)
    process_csv(sys.argv[1], sys.argv[2], sys.argv[3])
