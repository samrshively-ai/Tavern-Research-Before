"""
search_transcript.py

Searches a Whisper-style transcript JSON file for a phrase and returns the
timecodes and surrounding text of every matching segment.

Dependencies:
    - None beyond the Python standard library.
    - Expects a transcript JSON file with a top-level "segments" list, where
      each segment has "text", "start", and "end" fields (this is the
      standard output format from OpenAI Whisper / faster-whisper).

Usage:
    python search_transcript.py <transcript.json> <phrase>

Arguments:
    transcript.json   Path to a Whisper-format transcript JSON file
    phrase             Phrase to search for (case-insensitive, substring match)

Output:
    Prints each matching segment's start/end timecode (HH:MM:SS.mmm) and the
    full text of that segment to stdout. Prints "no matches" if none found.

Example:
    python search_transcript.py interview_transcript.json "Social Security"
"""

import json
import sys
import re
from pathlib import Path


def find_phrase_in_transcript(transcript_path, phrase, context_words=8):
    """
    given a whisper transcript json file and a phrase,
    return list of (start_time, end_time, surrounding_text) tuples.
    """
    with open(transcript_path) as f:
        data = json.load(f)

    matches = []
    phrase_lower = phrase.lower()

    segments = data.get("segments", [])
    for seg in segments:
        text = seg.get("text", "")
        if phrase_lower in text.lower():
            start = seg.get("start", 0)
            end = seg.get("end", 0)
            matches.append({
                "start": start,
                "end": end,
                "start_tc": seconds_to_tc(start),
                "end_tc": seconds_to_tc(end),
                "text": text.strip(),
            })

    return matches


def seconds_to_tc(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}"


def main():
    if len(sys.argv) < 3:
        print("usage: python search_transcript.py <transcript.json> <phrase>")
        sys.exit(1)

    path = sys.argv[1]
    phrase = sys.argv[2]

    matches = find_phrase_in_transcript(path, phrase)
    if not matches:
        print(f"no matches for '{phrase}'")
        return

    print(f"found {len(matches)} match(es) for '{phrase}':")
    for m in matches:
        print(f"  {m['start_tc']} - {m['end_tc']}: {m['text']}")


if __name__ == "__main__":
    main()
